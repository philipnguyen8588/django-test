from decimal import Decimal

from django.test import TestCase

from django_test.real_estate.models import Property, SaleType, Status
from django_test.real_estate.tests.factories import UserFactory


class ModelTests(TestCase):

    def setUp(self):
        self.test_user = UserFactory()

    def test_property_creation(self):
        property_data = {
            'address': "FPT Plaza 1 - Da Nang",
            'sale_type': SaleType.SALE,
            'status': Status.LEASED,
            'price': Decimal('30.02'),
            'created_by': self.test_user,
        }

        property_instance = Property.objects.create(
            **property_data
        )

        property = Property.objects.get(id=property_instance.id)

        self.assertEqual(property.address, property_data['address'])
        self.assertEqual(property.sale_type, property_data['sale_type'])
        self.assertEqual(property.status, property_data['status'])
        self.assertEqual(property.price, property_data['price'])
        self.assertEqual(property.created_by, property_data['created_by'])
        self.assertIsNotNone(property.created_at)
        self.assertIsNotNone(property.modified_at)
