from config.factories import ConfigFactory
from config.models import Config
from apis.api_device.tests.base import DeviceHeroAPITestCase, serialize_consumable_and_slot
from pills.models import Pill
from pills.factories import PillFactory
from rest_framework import status
from django.urls import reverse


class DeviceApiTestCase(DeviceHeroAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.config = ConfigFactory()
        cls.pill = PillFactory(device_config=cls.config)

        # Sending same data to test existing config
        pill_data = serialize_consumable_and_slot(cls.config, cls.pill)
        cls.right_payload = pill_data


class ConfigViewTestCase(DeviceApiTestCase):
    viewname = "device-config"

    def test_create_config_new_device(self):
        url = reverse("api_device:device-config")

        data = {
            "Table": {
                "device": {
                "device_id": 2,
                    "passcode": "1234",
                    "timezone_name": "America/New_York"
                },
                "consumables": [
                    {
                        "id": "id_1",
                        "name": "Vitamin C",
                        "expiration_date": "2020-03-14",
                        "dosage": "200 mg",
                        "passcode_mandatory": False,
                        "form": "Cap",
                        "max_doses": 4
                    }
                ],
                "slots": [
                    {
                        "slot_index": 1,
                        "consumable_id": "id_1",
                        "exact_pill_count": 20
                    }
                ]
            }
        }
        response = self.client.post(path=url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Config.objects.count(), 2)
        
        # Make sure created new Config object
        self.assertNotEqual(self.config.device_id, response.data["device_id"])
        self.assertNotEqual(self.config.pk, response.data["id"])

    def test_create_config_new_pill_data(self):
        url = reverse("api_device:device-config")

        data = {
            "Table": {
                "device": {
                "device_id": 1,
                    "passcode": "1234",
                    "timezone_name": "America/New_York"
                },
                "consumables": [
                    {
                        "id": "id_1",
                        "name": "Vitamin C",
                        "expiration_date": "2020-03-14",
                        "dosage": "200 mg",
                        "passcode_mandatory": False,
                        "form": "Cap",
                        "max_doses": 4
                    }
                ],
                "slots": [
                    {
                        "slot_index": 1,
                        "consumable_id": "id_1",
                        "exact_pill_count": 20
                    }
                ]
            }
        }

        response = self.client.post(path=url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Config.objects.count(), 2)

        # Make sure Config object stay same
        self.assertEqual(self.config.device_id, response.data["device_id"])
        self.assertEqual(self.config.is_active, True)
        self.assertNotEqual(self.config.pk, response.data["id"])

    def test_existing_old_config(self):
        url = reverse("api_device:device-config")

        response = self.client.post(path=url, data=self.right_payload, format="json")

        # Make sure new Config object is not created
        self.assertEqual(Config.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_config_with_many_pills(self):
        url = reverse("api_device:device-config")
        data = {
        "Table": {
            "device": {
                "device_id": 1,
                "passcode": "1234",
                "timezone_name": "America/New_York"
            },
            "consumables": [
                {
                    "id": "id_11",
                    "name": "Vitamin C",
                    "expiration_date": "2020-03-14",
                    "dosage": "200 mg",
                    "passcode_mandatory": False,
                    "form": "Cap",
                    "max_doses": 4
                },
            {
                    "id": "id_1",
                    "name": "Vitamin C",
                    "expiration_date": "2020-03-14",
                    "dosage": "200 mg",
                    "passcode_mandatory": False,
                    "form": "Cap",
                    "max_doses": 4
                }
            ],
            "slots": [
                {
                    "slot_index": 1,
                    "consumable_id": "id_1",
                    "exact_pill_count": 20
                },
            {
                    "slot_index": 1,
                    "consumable_id": "id_11",
                    "exact_pill_count": 100
                }
            ]
        }
        }

        response = self.client.post(path=url, data=data, format="json")

        # Make sure that old Pill stay in database, and new (2) Pills are created
        self.assertEqual(Pill.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_config_invalid_data(self):
        url = reverse("api_device:device-config")
        
        data = {
        "Table": {
            "device": {
            "device_id": 1,
                "passcode": "1234",
                "timezone_name": "America/New_York"
            },
            "consumables": [
                {
                    "id": "id_1",
                    "name": "Vitamin C",
                    "expiration_date": "2020-03-14",
                    "dosage": "200 mg",
                    "passcode_mandatory": False,
                    "form": "Cap",
                    "max_doses": 4
                }
            ],
            "slots": [
                {
                    "slot_index": 1,
                    "consumable_id": "id_115",
                    "exact_pill_count": 20
                },
            {
                    "slot_index": 1,
                    "consumable_id": "id_115",
                    "exact_pill_count": 20
                }
            ]
        }
        }

        response = self.client.post(path=url, data=data, format="json")

        self.assertEqual(Pill.objects.count(), 1)
        self.assertEqual(Config.objects.count(), 1)
