from django.test import TestCase

from .models import TestModel

# Create your tests here.
class TestBasicModel(TestCase):
    def setUp(self):
        self.t1 = TestModel.objects.create()
        self.t2 = TestModel.objects.create()
        self.t2.delete()

    def test_not_deleted_all(self):
        self.assertIn(self.t1, TestModel.objects.all())

    def test_not_deleted_filter(self):
        self.assertIn(self.t1, TestModel.objects.filter())
    
    def test_not_deleted_archive(self):
        self.assertIn(self.t1, TestModel.objects.archive())

    def test_deleted_all(self):
        self.assertNotIn(self.t2, TestModel.objects.all())

    def test_deleted_filter(self):
        self.assertNotIn(self.t2, TestModel.objects.filter())
    
    def test_deleted_archive(self):
        self.assertIn(self.t2, TestModel.objects.archive())
