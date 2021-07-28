from django.test import TestCase
from django.utils.timezone import now, timedelta

from ..models import *

# Create your tests here.
class TestDiscountModel(TestCase):
    def setUp(self):
        self.info = {
            'title_en': "Test",
            'title_fa': "تست",
            'slug': "test",
        }

    # tests for discount with toman unit and discount < price
    def test_toman_positive_1(self):
        d = Discount.objects.create(**self.info, unit='T', amount=5_000)
        self.assertEqual(d.calculate_price(75_000), 70_000)

    def test_toman_positive_2(self):
        d = Discount.objects.create(**self.info, unit='T', amount=25_000)
        self.assertEqual(d.calculate_price(55_000), 30_000)

    def test_toman_positive_3(self):
        d = Discount.objects.create(**self.info, unit='T', amount=7_000)
        self.assertEqual(d.calculate_price(17_500), 10_500)

    # tests for discount with toman unit and discount > price
    def test_toman_zero_1(self):
        d = Discount.objects.create(**self.info, unit='T', amount=12_000)
        self.assertEqual(d.calculate_price(10_000), 0)
    
    # tests for discount with percent unit and without ceiling value
    def test_percent_without_roof_1(self):
        d = Discount.objects.create(**self.info, unit='P', amount=12)
        self.assertEqual(d.calculate_price(250_000), 220_000)
    
    def test_percent_without_roof_2(self):
        d = Discount.objects.create(**self.info, unit='P', amount=50)
        self.assertEqual(d.calculate_price(100_000), 50_000)
    
    def test_percent_without_roof_3(self):
        d = Discount.objects.create(**self.info, unit='P', amount=2)
        self.assertEqual(d.calculate_price(12_000), 11_760)
    
    def test_percent_without_roof_4(self):
        d = Discount.objects.create(**self.info, unit='P', amount=15)
        self.assertEqual(d.calculate_price(1_000_000), 850_000)

    # tests for discount with percent unit and with ceiling value but less than
    def test_percent_with_roof_fewer_1(self):
        d = Discount.objects.create(**self.info, unit='P', amount=10, roof=20_000)
        self.assertEqual(d.calculate_price(120_000), 108_000)

    def test_percent_with_roof_fewer_2(self):
        d = Discount.objects.create(**self.info, unit='P', amount=5, roof=10_000)
        self.assertEqual(d.calculate_price(40_000), 38_000)

    def test_percent_with_roof_fewer_3(self):
        d = Discount.objects.create(**self.info, unit='P', amount=50, roof=25_000)
        self.assertEqual(d.calculate_price(20_000), 10_000)
    
    # tests for discount with percent unit and with ceiling value but not less than
    def test_percent_with_roof_bigger_1(self):
        d = Discount.objects.create(**self.info, unit='P', amount=25, roof=15_000)
        self.assertEqual(d.calculate_price(80_000), 65_000)
