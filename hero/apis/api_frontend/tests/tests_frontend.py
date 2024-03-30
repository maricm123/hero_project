from apis.api_frontend.tests.base import FrontendHeroAPITestCase, serialize_config, serialize_pill
from config.factories import ConfigFactory
from config.models import Config
from pills.models import Pill
from pills.factories import PillFactory
from rest_framework import status
from django.urls import reverse


class FrontendApiTestCase(FrontendHeroAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.config = ConfigFactory()
        cls.pill = PillFactory(device_config=cls.config)
        
        # Sending same data to test existing config
        pill_data = serialize_pill(cls.pill)
        device_data = serialize_config(cls.config)
        cls.right_payload = dict(
            device_data,
            pills = [pill_data]
        )


class ConfigViewTestCase(FrontendApiTestCase):
    viewname = "frontend-config"

    def test_create_config_new_device(self):
        url = reverse("api_frontend:frontend-config")

        data = {
            "device_id" : 2,
            "passcode": "1234",
            "timezone_name": "America/New_York",
            "pills": [
                {
                    "slot": "1",
                    "name": "Aspirin",
                    "dosage": "500mg",
                    "expires": "2024-03-19",
                    "passcode_required": "true",
                    "form": "Tablet",
                    "exact_pill_count": 10,
                    "max_manual_doses": 4
                }
            ]
            }
        response = self.client.post(path=url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Config.objects.count(), 2)
        # Make sure created new Config object
        self.assertNotEqual(self.config.device_id, response.data["device_id"])
        self.assertNotEqual(self.config.pk, response.data["id"])

    def test_create_config_new_pill_data(self):
        url = reverse("api_frontend:frontend-config")

        data = {
            "device_id" : 1,
            "passcode": "1234",
            "timezone_name": "America/New_York",
            "pills": [
                {
                    "slot": "1",
                    "name": "Brufen",
                    "dosage": "200mg",
                    "expires": "2024-03-19",
                    "passcode_required": "true",
                    "form": "Tablet",
                    "exact_pill_count": 20,
                    "max_manual_doses": 4
                }
            ]
        }

        response = self.client.post(path=url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Config.objects.count(), 2)
        # Make sure Config object stay same
        self.assertEqual(self.config.device_id, response.data["device_id"])
        self.assertEqual(self.config.is_active, True)
        self.assertNotEqual(self.config.pk, response.data["id"])

    def test_existing_old_config(self):
        url = reverse("api_frontend:frontend-config")

        response = self.client.post(path=url, data=self.right_payload, format="json")

        # Make sure new Config object is not created
        self.assertEqual(Config.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_config_with_many_pills(self):
        url = reverse("api_frontend:frontend-config")
        data = {
            "device_id" : 1,
            "passcode": "1234",
            "timezone_name": "America/New_York",
            "pills": [
                {
                    "slot": "1",
                    "name": "Aspirin",
                    "dosage": "500mg",
                    "expires": "2024-03-19",
                    "passcode_required": "true",
                    "form": "Tablet",
                    "exact_pill_count": 10,
                    "max_manual_doses": 4
                },
                {
                    "slot": "1",
                    "name": "Brufen",
                    "dosage": "200mg",
                    "expires": "2024-03-19",
                    "passcode_required": "true",
                    "form": "Tablet",
                    "exact_pill_count": 10,
                    "max_manual_doses": 4
                }
            ]
            }

        response = self.client.post(path=url, data=data, format="json")

        # Make sure that old Pill stay in database, and new (2) Pills are created
        self.assertEqual(Pill.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
