from django.test import TestCase

from django_test.real_estate.tests.factories import UserFactory

REAL_ESTATE_API_URL = '/api/real-estate/properties/'


class PropertyPermissionTests(TestCase):

    def setUp(self):
        self.login_user = UserFactory()
        self.other_user = UserFactory()

    def test_deletion_permission(self):
        self.client.force_login(self.login_user)
        # Create property
        data = {
                "address": "FPT Plaza 1 - Da Nang",
                "price": 100,
                "status": "AVAILABLE",
                "sale_type": "SALE",
            }
        create_response = self.client.post(
            REAL_ESTATE_API_URL,
            data=data
        )
        assert create_response.status_code == 201

        self.client.force_login(self.other_user)
        # DELETE property
        delete_response = self.client.delete(
            f'{REAL_ESTATE_API_URL}{create_response.json()["id"]}/'
        )

        assert delete_response.status_code == 403

    def test_update_permission(self):
        self.client.force_login(self.login_user)
        # Create property
        data = {
            "address": "FPT Plaza 1 - Da Nang",
            "price": 100,
            "status": "AVAILABLE",
            "sale_type": "SALE",
        }
        create_response = self.client.post(
            REAL_ESTATE_API_URL,
            data=data
        )
        assert create_response.status_code == 201

        self.client.force_login(self.other_user)
        # UPDATE property
        update_response = self.client.put(
            f'{REAL_ESTATE_API_URL}{create_response.json()["id"]}/',
            data=data
        )

        assert update_response.status_code == 403

    def test_patch_permission(self):
        self.client.force_login(self.login_user)
        # Create property
        data = {
            "address": "FPT Plaza 1 - Da Nang",
            "price": 100,
            "status": "AVAILABLE",
            "sale_type": "SALE",
        }
        create_response = self.client.post(
            REAL_ESTATE_API_URL,
            data=data
        )
        assert create_response.status_code == 201

        self.client.force_login(self.other_user)
        # PATCH property
        update_response = self.client.patch(
            f'{REAL_ESTATE_API_URL}{create_response.json()["id"]}/',
            data=data
        )

        assert update_response.status_code == 403
