from django.test import TestCase

from django_test.real_estate.tests.factories import UserFactory

REAL_ESTATE_API_URL = '/api/real-estate/properties/'


class PropertyApiTests(TestCase):

    def setUp(self):
        self.login_user = UserFactory()
        self.other_user = UserFactory()
        self.client.force_login(self.login_user)

    def test_creation_retrieve(self):
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
        # GET property
        get_response = self.client.get(
            f'{REAL_ESTATE_API_URL}{create_response.json()["id"]}/'
        )
        assert get_response.status_code == 200
        response_json = get_response.json()
        assert response_json['address'] == data['address']
        assert response_json['price'] == data['price']
        assert response_json['status'] == data['status']
        assert response_json['sale_type'] == data['sale_type']
        assert response_json['created_by'] == self.login_user.username

    def test_deletion(self):
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
        # DELETE property
        self.client.delete(
            f'{REAL_ESTATE_API_URL}{create_response.json()["id"]}/'
        )

        # GET property
        get_response = self.client.get(
            f'{REAL_ESTATE_API_URL}{create_response.json()["id"]}/'
        )
        assert get_response.status_code == 404

    def test_filter(self):
        # Create property
        datas = [
            {
                "address": "FPT Plaza 1 - Da Nang",
                "price": 100,
                "status": "AVAILABLE",
                "sale_type": "SALE",
            },
            {
                "address": "Ha noi",
                "price": 200,
                "status": "SOLD",
                "sale_type": "SALE",
            },
            {
                "address": "Quang nam",
                "price": 300,
                "status": "SOLD",
                "sale_type": "SALE",
            },
            {
                "address": "Hue",
                "price": 400,
                "status": "LEASED",
                "sale_type": "LEASE",
            },
            {
                "address": "Da Nang - Vietnam",
                "price": 500,
                "status": "AVAILABLE",
                "sale_type": "LEASE",
            },
            {
                "address": "Quang Binh - Vietnam",
                "price": 500,
                "status": "DELETED",
                "sale_type": "SALE",
            },
        ]
        for data in datas:
            self.client.post(
                REAL_ESTATE_API_URL,
                data=data
            )

        # filter exclude DELETED
        response = self.client.get(REAL_ESTATE_API_URL)
        assert response.status_code == 200 and response.json()['total_items'] == 5

        # filter include DELETED
        response = self.client.get(REAL_ESTATE_API_URL, data={
            'include_deleted': True
        })
        assert response.status_code == 200 and response.json()['total_items'] == 6

        # filter price
        response = self.client.get(REAL_ESTATE_API_URL, data={
            'price_gte': 200,
            'price_lte': 400,
        })
        assert response.status_code == 200 and response.json()['total_items'] == 3

        # filter address
        response = self.client.get(REAL_ESTATE_API_URL, data={
            'address': 'Da nang',
        })
        assert response.status_code == 200 and response.json()['total_items'] == 2

        # filter status
        response = self.client.get(REAL_ESTATE_API_URL, data={
            'status': 'SOLD',
        })
        assert response.status_code == 200 and response.json()['total_items'] == 2

        # filter status
        response = self.client.get(REAL_ESTATE_API_URL, data={
            'sale_type': 'LEASE',
        })
        assert response.status_code == 200 and response.json()['total_items'] == 2

