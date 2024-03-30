from rest_framework import serializers
from apis.api_frontend.serializers.serializers_config import PillSerializer
from config.models import Config


class ConfigOutSerializer(serializers.ModelSerializer):
    pills = PillSerializer(many=True)

    class Meta:
        model = Config
        fields = ("id", "device_id", "passcode", "timezone_name", "is_active", "pills",)
