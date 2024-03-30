import factory
from pills.models import Pill


class PillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pill
    
    slot = "1"
    name = "Brufen"
    dosage = "200mg"
    expires = factory.Faker('date_object')
    passcode_required = False
    form = "Cap"
    exact_pill_count = 10
    max_manual_doses = 4
    device_config = factory.SubFactory("config.factories.ConfigFactory")
