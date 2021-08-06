from django.test import TestCase
from django.db import transaction
from django.db.utils import IntegrityError

from ..models import Customer, Address

# Create your tests here.
class TestAddressModel(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(username="test", password="test4321")
        self.home = Address.objects.create(customer=self.customer, name="Home",
            zip_code="1234567890", province="Tehran", city="Tehran",
            rest="...", lat=35.56, lng=54.35)

    def test_successfully_add_address(self):
        self.assertEqual(self.home.customer, self.customer)

    def test_successfully_add_new_address(self):
        work = Address.objects.create(customer=self.customer, name="Work",
            zip_code="1234567891", province="Tehran", city="Tehran",
            rest="...", lat=35.65, lng=54.53)
        self.assertIn(work, self.customer.addresses.all())

    def test_duplicated_address_adding(self):
        try:  # try to add duplicate address for check unique together lat & lng
            # This is caused by a quirk in how transactions are handled in Django
            with transaction.atomic():
                Address.objects.create(customer=self.customer, name="House",
                    zip_code="1234567892", province="Tehran", city="Tehran",
                    rest="...", lat=35.56, lng=54.35)
        except IntegrityError:
            pass
        self.assertEqual(self.customer.addresses.all().count(), 1)  # not appending
