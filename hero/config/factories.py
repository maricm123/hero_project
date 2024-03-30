import factory
from config.models import Config


class ConfigFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Config

    device_id = 1
    passcode = "1234"
    timezone_name = "America/New_York"
    is_active = True
