from django.test import TestCase
from django.utils.timezone import now, timedelta

from ..models import Customer

# Create your tests here.
class TestCustomerModel(TestCase):
    def test_age_zero(self):
        self.customer = Customer.objects.create(username="test", password="test4321")
        self.customer.birth_day = now() - timedelta(days=364)
        self.customer.save()
        self.assertEqual(self.customer.age, 0)
    
    def test_age_positive(self):
        self.customer = Customer.objects.create(username="test", password="test4321")
        self.customer.birth_day = now() - timedelta(days=7559)
        self.customer.save()
        self.assertEqual(self.customer.age, 20)
    
    def test_age_null(self):
        self.customer = Customer.objects.create(username="test", password="test4321")
        self.assertIsNone(self.customer.age)
