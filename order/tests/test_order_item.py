from django.test import TestCase
from django.utils.timezone import now, timedelta

from customer.models import *
from product.models import *
from ..models import *

# Create your tests here.
class TestOrderItemModel(TestCase):
    def setUp(self):
        # created customers
        self.one = Customer.objects.create(username="09123456789", password="1O1nn1e1e")
        self.two = Customer.objects.create(username="09123456788", password="1O1nn1e1e")
        self.three = Customer.objects.create(username="09123456787", password="1O1nn1e1e")
        self.four = Customer.objects.create(username="09123456786", password="1O1nn1e1e")
        self.five = Customer.objects.create(username="09123456785", password="1O1nn1e1e")
        self.six = Customer.objects.create(username="09123456784", password="1O1nn1e1e")
        self.seven = Customer.objects.create(username="09123456783", password="1O1nn1e1e")
        self.eight = Customer.objects.create(username="09123456782", password="1O1nn1e1e")
        self.nine = Customer.objects.create(username="09123456781", password="1O1nn1e1e")

        # created discounts
        self.d1 = Discount.objects.create(title_en="Mobile", title_fa="موبایل",
                                            slug="mobile", unit='P', amount=10)
        self.d2 = Discount.objects.create(title_en="Lebas Shoie", title_fa="لباس شویی",
                                            slug="lebas-shoie", unit='T', amount=25_000)
        self.d3 = Discount.objects.create(title_en="Medad", title_fa="مداد",
                                            slug="medad", unit='P', amount=20)
        
        self.x = DiscountCode.objects.create(title_en="XYZ1", title_fa="ایکس",
            slug="xyz1", unit='P', amount=10, roof=5_000, code="xyz1")
        self.y = DiscountCode.objects.create(title_en="XYZ2", title_fa="وای",
            slug="xyz2", unit='P', amount=5, roof=20_000, code="xyz2")
        self.z = DiscountCode.objects.create(title_en="XYZ3", title_fa="زد",
            slug="xyz3", unit='P', amount=20, roof=20_000, code="xyz3")
        self.w = DiscountCode.objects.create(title_en="XYZ4", title_fa="دابلیو",
            slug="xyz4", unit='P', amount=10, roof=30_000, code="xyz4")
        
        # created products
        self.brand = Brand.objects.create(title_en="Farzane", title_fa="فرزانه", slug="farzane")
        self.category = Category.objects.create(title_en="Sepehr", title_fa="سپهر",slug="sepehr")

        self.mobile = Product.objects.create(title_en="Mobile", title_fa="موبایل",
            slug="mobile", brand=self.brand, category=self.category,
            discount=self.d1, price=50_000, inventory=20)
        self.lebas = Product.objects.create(title_en="Lebas Shoie", title_fa="لباس شویی",
            slug="lebas-shoie", brand=self.brand, category=self.category,
            discount=self.d2, price=500_000, inventory=20)
        self.medad = Product.objects.create(title_en="Medad", title_fa="مداد",
            slug="medad", brand=self.brand, category=self.category,
            discount=self.d3, price=1_000, inventory=40)
        self.daftar = Product.objects.create(title_en="Daftar", title_fa="دفتر",
            slug="daftar", brand=self.brand, category=self.category, price=5_000, inventory=40)

    def test_successfully_order_1(self):
        o = Order.objects.create(customer=self.one, code="xyz1")
        OrderItem.objects.create(order=o, product=self.mobile, count=2)
        OrderItem.objects.create(order=o, product=self.medad, count=4)
        o.payment()
        self.assertEqual(o.total_price, 104_000)
        self.assertEqual(o.final_price, 88_200)
        self.assertEqual(o.items.all()[0].product.inventory, 18)
        self.assertEqual(o.items.all()[1].product.inventory, 36)

