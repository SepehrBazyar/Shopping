from django.test import TestCase

from customer.models import *
from product.models import *
from .models import *

# Create your tests here.
class TestOrderItemModel(TestCase):
    def setUp(self):
        # created customers
        self.customer = Customer.objects.create(username="09123456789", password="1O1nn1e1e")

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
        o = Order.objects.create(customer=self.customer, code="xyz1")
        OrderItem.objects.create(order=o, product=self.mobile, count=2)
        OrderItem.objects.create(order=o, product=self.medad, count=4)
        o.payment()
        self.assertEqual(o.total_price, 104_000)
        self.assertEqual(o.final_price, 88_200)
        self.assertEqual(o.items.all()[0].product.inventory, 18)
        self.assertEqual(o.items.all()[1].product.inventory, 36)

    def test_canceling_order_1(self):
        o = Order.objects.create(customer=self.customer, code="xyz2")
        OrderItem.objects.create(order=o, product=self.lebas, count=1)
        o.payment()
        self.assertEqual(o.total_price, 500_000)
        self.assertEqual(o.final_price, 455_000)
        self.assertEqual(o.items.all()[0].product.inventory, 19)
        o.cancel()
        self.assertEqual(o.items.all()[0].product.inventory, 20)

    def test_unpaid_order_1(self):
        o = Order.objects.create(customer=self.customer, code="xyz4")
        OrderItem.objects.create(order=o, product=self.mobile, count=3)
        OrderItem.objects.create(order=o, product=self.lebas, count=2)
        OrderItem.objects.create(order=o, product=self.medad, count=8)
        OrderItem.objects.create(order=o, product=self.daftar, count=7)
        self.assertEqual(o.total_price, 1_193_000)
        self.assertEqual(o.final_price, 1_096_400)
        self.assertEqual(o.items.all()[0].product.inventory, 20)
        self.assertEqual(o.items.all()[1].product.inventory, 20)
        self.assertEqual(o.items.all()[2].product.inventory, 40)
        self.assertEqual(o.items.all()[3].product.inventory, 40)

    def test_without_discount_code_1(self):
        o = Order.objects.create(customer=self.customer)
        OrderItem.objects.create(order=o, product=self.mobile, count=1)
        OrderItem.objects.create(order=o, product=self.daftar, count=10)
        o.payment()
        self.assertEqual(o.total_price, 100_000)
        self.assertEqual(o.final_price, 95_000)
        self.assertEqual(o.items.all()[0].product.inventory, 19)
        self.assertEqual(o.items.all()[1].product.inventory, 30)
    
    def test_not_enough_inventory_1(self):
        o = Order.objects.create(customer=self.customer)
        try:
            OrderItem.objects.create(order=o, product=self.mobile, count=21)
        except ValueError:
            pass
        OrderItem.objects.create(order=o, product=self.lebas, count=20)
        o.payment()
        self.assertEqual(o.items.all().count(), 1)
        self.assertEqual(o.total_price, 10_000_000)
        self.assertEqual(o.final_price, 9_500_000)

    def test_not_enough_inventory_2(self):
        o = Order.objects.create(customer=self.customer, code="xyz4")
        try:
            OrderItem.objects.create(order=o, product=self.medad, count=41)
        except ValueError:
            pass
        try:
            OrderItem.objects.create(order=o, product=self.daftar, count=42)
        except ValueError:
            pass
        o.payment()
        self.assertEqual(o.items.all().count(), 0)
        self.assertEqual(o.total_price, 0)
        self.assertEqual(o.final_price, 0)

    def test_duplicate_discount_code_1(self):
        self.test_canceling_order_1()
        o = Order.objects.create(customer=self.customer, code="xyz2")
        OrderItem.objects.create(order=o, product=self.lebas, count=1)
        OrderItem.objects.create(order=o, product=self.mobile, count=1)
        OrderItem.objects.create(order=o, product=self.daftar, count=3)
        o.payment()
        self.assertEqual(o.total_price, 565_000)
        self.assertEqual(o.final_price, 515_000)
        self.assertEqual(o.items.all()[0].product.inventory, 19)
        self.assertEqual(o.items.all()[1].product.inventory, 19)
        self.assertEqual(o.items.all()[2].product.inventory, 37)
    
    def test_duplicate_discount_code_2(self):
        self.test_successfully_order_1()
        try:
            o = Order.objects.create(customer=self.customer, code="xyz1")
        except ValueError:
            o = Order.objects.create(customer=self.customer)
        OrderItem.objects.create(order=o, product=self.medad, count=4)
        OrderItem.objects.create(order=o, product=self.lebas, count=1)
        o.payment()
        self.assertEqual(o.total_price, 504_000)
        self.assertEqual(o.final_price, 478_200)
        self.assertEqual(o.items.all()[0].product.inventory, 32)
        self.assertEqual(o.items.all()[1].product.inventory, 19)
    
    def test_other_discount_code_1(self):
        self.test_successfully_order_1()
        try:
            o = Order.objects.create(customer=self.customer, code="xyz3")
        except ValueError:
            o = Order.objects.create(customer=self.customer)
        OrderItem.objects.create(order=o, product=self.medad, count=4)
        OrderItem.objects.create(order=o, product=self.lebas, count=1)
        o.payment()
        self.assertEqual(o.total_price, 504_000)
        self.assertEqual(o.final_price, 458_200)
        self.assertEqual(o.items.all()[0].product.inventory, 32)
        self.assertEqual(o.items.all()[1].product.inventory, 19)

    def test_invalid_discount_code_1(self):
        try:
            o = Order.objects.create(customer=self.customer, code="xyz6")
        except ValueError:
            o = Order.objects.create(customer=self.customer)
        OrderItem.objects.create(order=o, product=self.mobile, count=6)
        OrderItem.objects.create(order=o, product=self.medad, count=10)
        o.payment()
        self.assertEqual(o.total_price, 310_000)
        self.assertEqual(o.final_price, 278_000)
        self.assertEqual(o.items.all()[0].product.inventory, 14)
        self.assertEqual(o.items.all()[1].product.inventory, 30)
