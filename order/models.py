from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from typing import Tuple

from core.models import BasicModel
from core.utils import readable
from customer.models import Address, Customer
from product.models import Discount, Product
from .validators import CountValidator, CustomerAddressValidator, DiscountCodeValidator

# Create your models here.
class DiscountCode(Discount):
    """
    Model of Discount Code for Apply on Order Price After Check Validated
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Discount Code"), _("Discount Codes")

    code = models.CharField(max_length=10, unique=True, verbose_name=_("Identification Code"),
        help_text=_("Please Enter Identification Code to Check Validation in Order Model"))
    users = models.ManyToManyField(Customer, related_name="codes", default=None, null=True,
        verbose_name=_("Users Used"), help_text=_("Show Which Users have Used this Code?"))

    def __str__(self) -> str:
        return f"{self.code} - {super().__str__()}"


class Order(BasicModel):
    """
    Model of Order or Recepite Collection of Many Order Items
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Order"), _("Orders")

    STATUSES = {
        'P': _("Paid"),
        'U': _("Unpaid"),
        'C': _("Canceled")
    }

    status = models.CharField(max_length=1, default='U', verbose_name=_("Status of Order"), 
        choices=[(key, value) for key, value in STATUSES.items()],
        help_text=_("Please Select the Status of Order(By Default Unpaid is Considered)"))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders",
        verbose_name=_("Customer"), help_text=_("Please Select Customer Owner this Order"))
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='+',
        verbose_name=_("Address"), help_text=_("Please Select Address to Send Order There"))
    total_price = models.PositiveBigIntegerField(default=0, verbose_name=_("Total Price"),
        help_text=_("Total Price is Sum of Pure Price of Product Items for this Order"))
    final_price = models.PositiveBigIntegerField(default=0, verbose_name=_("Final Price"),
        help_text=_("Final Price is Sum of Price of Product Items for this Order After Dicount"))
    code = models.CharField(max_length=10, default=None, null=True, blank=True,
        verbose_name=_("Discount Code"), help_text=_("If You have a Discount Code Please Enter it"))
    discount = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, blank=True,
        related_name='+', default=None, null=True, verbose_name=_("Discount Value"),
        help_text=_("Please Select Discount from Discount Codes to Apply on Price"))

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        if self.code is None: self.discount = None  # if customer remove code
        else:  # update discount code in start initialize
            discode = DiscountCode.objects.filter(code__exact=self.code)
            if discode.count() == 1: self.discount = DiscountCode.objects.get(code=self.code)
            else: self.code = None  # if code is invalid clear code field in database
        self.total_price, self.final_price = self.update_price()  # check changes
        self.__pre_discount = self.discount  # for check changed value in save method
        self.__pre_status = self.status  # for check payment or canceling order
        if self.status == 'U':
            for item in self.items.all():  # remove items from order if count not enough
                if item.count > item.product.inventory: item.delete()
    
    @classmethod
    def total_income(cls) -> int:
        """
        Class Method Function for Sum of Total Incoming of All Paid Orders
        """

        result = cls.objects.filter(status__exact='P').aggregate(models.Sum('final_price'))
        return result["final_price__sum"]

    @property
    def readable_total_price(self):
        """
        Make Readable Form of Total Price for Show in Template Pages
        """

        return readable(self.total_price)
    
    @property
    def readable_final_price(self):
        """
        Make Readable Form of Final Price for Show in Template Pages
        """

        return readable(self.final_price)
    
    @property
    def status_name(self):
        """
        Make Readable Form of Final Price for Show in Template Pages
        """

        return self.__class__.STATUSES[self.status]
    
    @property
    def paid(self):
        """
        Check Paid Order for Canceling in Orders List View Page
        """

        return self.status == 'P'

    def payment(self):
        """
        Method to Payment Order & Change Status & Update Inventory Number
        """

        if self.discount is not None:  # expired discount code for this customer
            if self.customer in self.discount.users.all():
                self.discount = None  # discount code used already
                self.total_price, self.final_price = self.update_price()
            else:
                self.discount.users.add(self.customer)
        for item in self.items.all():  # decrease from inventory in database
            try: item.product.change_inventory(item.count)
            except ValueError: item.delete()
        self.status = 'P'
    
    def cancel(self):
        """
        Method to Cancel Order & Change Status & Update Inventory Number
        """

        if self.__pre_status == 'P':  # if before paid and decrease from inventory back change
            if self.discount is not None:  # unexpire discount because not paid
                self.discount.users.remove(self.customer)
            for item in self.items.all():
                item.product.change_inventory(-item.count)  # negative number add to inventory
        self.status = 'C'

    def update_price(self) -> Tuple[int, int]:
        """
        Update Prices of Order by Any Change Return Total Price then Final Price
        """

        # total price is sum of pure price and final price after apply both discounts
        total_price, final_price = 0, 0
        for item in self.items.all():
            total_price += item.count * item.product.price
            final_price += item.count * item.product.final_price
        if self.discount is not None:
            final_price = self.discount.calculate_price(final_price)
        return total_price, final_price

    def clean(self):  # clean data from get any form and check discount code value
        if self.code is not None and self.status != 'C':
            discode = DiscountCode.objects.filter(code__exact=self.code)
            DiscountCodeValidator(discode)(self.customer)
        try:CustomerAddressValidator(self.customer)(self.address)
        except ObjectDoesNotExist: pass

    def save(self, *args, **kwargs):
        # just save changes in this states: not paid yet or canceling paid orders
        if self.__pre_status == 'U' or (self.__pre_status == 'P' and self.status == 'C'):
            if self.status == 'C': self.cancel()
            elif self.status == 'P': self.payment()
            elif self.discount != self.__pre_discount:  # enter new discount code
                self.final_price = self.discount.calculate_price(self.final_price)
            else:  # in this state change is adding new item in other model
                self.total_price, self.final_price = self.update_price()
            if self.code is not None and self.discount is None:
                self.discount = DiscountCode.objects.get(code=self.code)
                self.final_price = self.discount.calculate_price(self.final_price)
            return super(self.__class__, self).save(*args, **kwargs) 

    def __str__(self) -> str:
        toman_trans = _("Toman")
        return f"{self.customer.username} - \
            {readable(self.final_price)} {toman_trans} - \
            {self.__class__.STATUSES[self.status]}"


class OrderItem(BasicModel):
    """
    Model of Order Items for Connect to Recepite Order & Product Items
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Order Item"), _("Order Items")

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items",
        verbose_name=_("Recepite Order"), help_text=_("Please Select Your Order"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+',
        verbose_name=_("Product Item"), help_text=_("Please Select Product Item to Add"))
    count = models.PositiveIntegerField(default=1,
        verbose_name=_("Count of Order Item"), validators=[MinValueValidator(1)],
        help_text=_("Please Selcet the Count of this Order Item(Minimum Value is 1)."))

    def clean(self):  # clean data from get any form and check inventory value
        if self.order.status == 'U':
            CountValidator(self.product)(self.count)

    def save(self, *args, **kwargs):
        if self.order.status == 'U':  # just parent order not paid save changes
            result = super(self.__class__, self).save(*args, **kwargs)
            self.order.save()  # update the parent order by change in this item
            return result

    def __str__(self) -> str:
        return f"{self.order.id} - {self.product.title} - {self.count}"
