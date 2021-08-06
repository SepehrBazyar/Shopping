from django.test import TestCase
from django.utils.timezone import now, timedelta

from customer.models import *
from product.models import *
from ..models import *

# Create your tests here.
class TestOrderModel(TestCase):
    def setUp(self):
        pass
