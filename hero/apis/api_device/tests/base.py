from rest_framework.test import APITestCase


class DeviceHeroAPITestCase(APITestCase):
    namespace = "api_device"

def serialize_consumable_and_slot(config, pill):
    return {
        "Table": {
            "device": {
                "device_id": config.device_id,
                "passcode": config.passcode,
                "timezone_name": config.timezone_name,
            },
            "consumables": [
            {
                "id": "id_1",
                "name": pill.name,
                "expiration_date": pill.expires,
                "dosage": pill.dosage,
                "passcode_mandatory": pill.passcode_required,
                "form": pill.form,
                "max_doses": pill.max_manual_doses
            }
            ],
            "slots": [
                {
                    "slot_index": pill.slot,
                    "consumable_id": "id_1",
                    "exact_pill_count": pill.exact_pill_count
                }
            ]
        }
    }
