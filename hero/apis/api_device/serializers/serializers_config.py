from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
from config.models import Config
from apis.utils import check_same_pill_and_slot, count_pills_from_request
from pills.models import Pill


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ("device_id", "passcode", "timezone_name",)


class PillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pill
        fields = (
            "id",
            "name",
            "dosage",
            "form",
            "expiration_date",
            "passcode_mandatory",
            "max_doses",
        )

    id = serializers.CharField()
    expiration_date = serializers.DateField(source='expires')
    passcode_mandatory = serializers.BooleanField(source='passcode_required')
    max_doses = serializers.IntegerField(source='max_manual_doses')

    def validate_id(self, value):
        pill_id = int(value.split('_')[1])
        return pill_id


class SlotSerializer(serializers.ModelSerializer):
    slot_index = serializers.CharField(source="slot", required=True)
    consumable_id = serializers.CharField(source="id", required=True)

    class Meta:
        model = Pill
        fields = ('slot_index', "consumable_id", "exact_pill_count")

    def validate_consumable_id(self, value):
        consumable_id = int(value.split('_')[1])
        return consumable_id


class TableSerializer(serializers.Serializer):
    device = DeviceSerializer()
    consumables = PillSerializer(many=True)
    slots = SlotSerializer(many=True)

    def validate(self, data):
        device_id = data["device"]["device_id"]
        consumable_and_slot_pair = check_same_pill_and_slot(data)
        try:
            config = Config.objects.get_active_config(device_id)
            return self.check_and_update_config(data, config, consumable_and_slot_pair)
        except Config.DoesNotExist:
            new_config = self.create_config_and_pills(
                data, consumable_and_slot_pair
            )
            data["pk"] = new_config.pk
            return data
        except Config.MultipleObjectsReturned:
            raise ValidationError("Multiple Config objects returned!")

    def check_and_update_config(self, data, config, consumable_and_slot_pair):
        pills = Pill.objects.get_device_configs(device_config=config)
        pills_from_request = count_pills_from_request(data)
        pills_from_database = pills.count()

        # If there is not same number of pills (from database and from request), create new config
        if pills_from_request != pills_from_database:
            new_config = self.create_config_and_pills(data, consumable_and_slot_pair)
            data["pk"] = new_config.pk

        else:
            diffrence_found = False
            for i, pill in enumerate(pills):
                if i < len(consumable_and_slot_pair):
                    json_pill = consumable_and_slot_pair[i]
                    if (
                        pill.name == json_pill["name"] and
                        pill.dosage == json_pill["dosage"] and
                        pill.expires == json_pill["expires"] and
                        pill.passcode_required == json_pill["passcode_required"] and
                        pill.form == json_pill["form"] and
                        pill.exact_pill_count == json_pill["exact_pill_count"] and
                        pill.slot == json_pill["slot"] and
                        pill.max_manual_doses == json_pill["max_manual_doses"]
                    ):
                        data["old_config"] = config.pk
                    else:
                        diffrence_found = True
                else:
                    raise ValidationError("Error with index")
            if diffrence_found:
                new_config = self.create_config_and_pills(data, consumable_and_slot_pair)
                data["pk"] = new_config.pk
        return data

    @transaction.atomic
    def create_config_and_pills(self, data, consumable_and_slot_pair):
        new_config = Config.create(
            device_id=data["device"]["device_id"],
            passcode=data["device"]["passcode"],
            timezone_name=data["device"]["timezone_name"],
        )
        Pill.create(
            pills=consumable_and_slot_pair,
            config=new_config,
        )
        return new_config
