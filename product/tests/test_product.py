from django.test import TestCase

from ..models import *

# Create your tests here.
class TestProductModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title_en="Test", title_fa="تست", slug="test")
        self.brand = Brand.objects.create(title_en="Test", title_fa="تست", slug="test")
        self.discount = Discount.objects.create(title_en="Test", title_fa="تست", slug="test",
                                                unit='P', amount=10, roof=20_000)

    # tests for product final price when product item has a discount
    def test_product_with_discount_1(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=120_000,
            inventory=1_000, category=self.category, brand=self.brand, discount=self.discount)
        self.assertEqual(p.final_price, 108_000)
    
    # tests for product final price when product item hasn't a discount
    def test_product_without_discount_1(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=120_000,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertEqual(p.final_price, 120_000)
