from django.test import TestCase
from django.utils.timezone import now, timedelta

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
    
    # tests for check is apply discount on price product or expire date time
    def test_product_check_discount_false_1(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=120_000,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertFalse(p.check_discount)
    
    def test_product_check_discount_false_2(self):
        self.discount.end_date = now() - timedelta(days=1)
        self.discount.save()  #expired discount by yesterday date time field

        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=120_000,
            inventory=1_000, category=self.category, brand=self.brand, discount=self.discount)
        self.assertFalse(p.check_discount)
    
    def test_product_check_discount_false_3(self):
        self.discount.start_date = now() + timedelta(days=1)
        self.discount.save()  #not started yet discount by tomorrow date time field

        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=120_000,
            inventory=1_000, category=self.category, brand=self.brand, discount=self.discount)
        self.assertFalse(p.check_discount)

    def test_product_check_discount_true_1(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=120_000,
            inventory=1_000, category=self.category, brand=self.brand, discount=self.discount)
        self.assertTrue(p.check_discount)

    # tests for readable method use the func in utils and seprate 3 digits with / char
    def test_product_readable_price_6_digits_1(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=128_500,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertEqual(p.readable_price, "128/500")
    
    def test_product_readable_price_6_digits_2(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=370_000,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertEqual(p.readable_price, "370/000")
    
    def test_product_readable_price_5_digits_1(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=25_750,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertEqual(p.readable_price, "25/750")
    
    def test_product_readable_price_5_digits_2(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=14_000,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertEqual(p.readable_price, "14/000")
    
    def test_product_readable_price_4_digits_1(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=7_750,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertEqual(p.readable_price, "7/750")
    
    def test_product_readable_price_4_digits_2(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=1_020,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertEqual(p.readable_price, "1/020")
    
    def test_product_readable_price_3_digits_1(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=700,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertEqual(p.readable_price, "700")
    
    def test_product_readable_price_2_digits_1(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=25,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertEqual(p.readable_price, "25")
    
    def test_product_readable_price_7_digits_1(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=1_324_000,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertEqual(p.readable_price, "1/324/000")
    
    def test_product_readable_price_8_digits_1(self):
        p = Product.objects.create(title_en="Test", title_fa="تست", slug="test", price=14_782_000,
            inventory=1_000, category=self.category, brand=self.brand)
        self.assertEqual(p.readable_price, "14/782/000")

    def tearDown(self):  # end of any test function for delete in db
        with MongoClient('mongodb://localhost:27017/') as client:
            categories = client.shopping.categories
            result = categories.delete_one({
                "_id": ObjectId(self.category.properties)
            })
        self.assertEqual(result.deleted_count, 1)
