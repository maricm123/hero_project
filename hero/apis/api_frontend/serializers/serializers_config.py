from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from config.models import Config
from apis.utils import count_pills_from_request
from pills.models import Pill
from django.db import transaction


class PillSerializer(serializers.ModelSerializer):
    expires = serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = Pill
        fields = ("slot", "name", "dosage", "expires", "passcode_required", "form", "exact_pill_count", "max_manual_doses",)


class ConfigSerializer(serializers.Serializer):
    device_id = serializers.IntegerField()
    passcode = serializers.CharField()
    timezone_name = serializers.CharField()
    pills = PillSerializer(many=True)

    def validate(self, data):
        device_id = data["device_id"]
        try:
            config = Config.objects.get_active_config(device_id)
        except Config.DoesNotExist:
            new_config = self.create_config_and_pills(data)
            data["pk"] = new_config.pk
            return data
        except Config.MultipleObjectsReturned:
            raise ValidationError("Multiple Config objects returned!")

        return self.check_and_update_config(data, config)

    def check_and_update_config(self, data, config):
        pills = Pill.objects.get_device_configs(device_config=config)
        json_pills = data.get("pills", [])
        pills_from_request = count_pills_from_request(data)
        pills_from_database = pills.count()

        if pills_from_request != pills_from_database:
            new_config = self.create_config_and_pills(data)
            data["pk"] = new_config.pk
        else:
            diffrence_found = False
            for i, pill in enumerate(pills):
                if i < len(json_pills):
                    json_pill = json_pills[i]
                    if (
                        pill.slot == json_pill["slot"]
                        and pill.name == json_pill["name"]
                        and pill.dosage == json_pill["dosage"]
                        and pill.expires == json_pill["expires"]
                        and pill.passcode_required == json_pill["passcode_required"]
                        and pill.form == json_pill["form"]
                        and pill.exact_pill_count == json_pill["exact_pill_count"]
                        and pill.max_manual_doses == json_pill["max_manual_doses"]
                    ):
                        data["old_config"] = config.pk
                    else:
                        diffrence_found = True
                else:
                    raise ValidationError("Error with index")
            if diffrence_found:
                new_config = self.create_config_and_pills(data)
                data["pk"] = new_config.pk
        return data

    @transaction.atomic
    def create_config_and_pills(self, data):
        new_config = Config.create(
            device_id=data["device_id"],
            passcode=data["passcode"],
            timezone_name=data["timezone_name"],
        )
        Pill.create(
            pills=data["pills"],
            config=new_config
        )
        return new_config
