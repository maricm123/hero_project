from rest_framework.test import APITestCase


class FrontendHeroAPITestCase(APITestCase):
    namespace = "api_frontend"


def serialize_config(config):
    return dict(
        device_id=config.device_id,
        passcode=config.passcode,
        timezone_name=config.timezone_name,
        is_active=config.is_active,
    )

def serialize_pill(pill):
    return dict(
        slot=pill.slot,
        name=pill.name,
        dosage=pill.dosage,
        expires=pill.expires,
        passcode_required=pill.passcode_required,
        form=pill.form,
        exact_pill_count=pill.exact_pill_count,
        max_manual_doses=pill.max_manual_doses,
        device_config=serialize_config(pill.device_config),
    )
