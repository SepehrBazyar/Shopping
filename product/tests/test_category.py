from django.test import TestCase

from pymongo import MongoClient
from bson.objectid import ObjectId

from ..models import *

# Create your tests here.
class TestCategoryModel(TestCase):
    def setUp(self):
        self.c = Category.objects.create(title_en="Test", title_fa="تست", slug="test")

    # tests for read and add and delete in property list category in mongodb nosql
    def test_read_1(self):
        self.assertListEqual(self.c.property_list(), [])

    def test_add_1_default(self):
        self.c.add_property("Test", "تست")
        self.assertListEqual(self.c.property_list(), ["تست"])
    
    def test_add_2_fa(self):
        self.c.add_property("Test", "تست")
        self.assertListEqual(self.c.property_list('fa'), ["تست"])

    def test_add_3_en(self):
        self.c.add_property("Test", "تست")
        self.assertListEqual(self.c.property_list('en'), ["Test"])

    def test_delete_1_default(self):
        self.c.add_property("Test", "تست")
        self.c.delete_property("تست")
        self.assertListEqual(self.c.property_list(), [])
    
    def test_delete_2_fa(self):
        self.c.add_property("Test", "تست")
        self.c.delete_property("تست", 'fa')
        self.assertListEqual(self.c.property_list('fa'), [])
    
    def test_delete_3_en(self):
        self.c.add_property("Test", "تست")
        self.c.delete_property("Test", 'en')
        self.assertListEqual(self.c.property_list(), [])
    
    def test_delete_4_except(self):
        self.c.add_property("Test", "تست")
        self.c.delete_property("Akbar")
        self.assertListEqual(self.c.property_list('fa'), ["تست"])

    def tearDown(self):  # end of any test function for delete in db
        with MongoClient('mongodb://localhost:27017/') as client:
            categories = client.shopping.categories
            result = categories.delete_one({
                "_id": ObjectId(self.c.properties)
            })
        self.assertEqual(result.deleted_count, 1)
