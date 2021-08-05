from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BasicModel
from core.utils import readable
from customer.models import Customer
from product.models import Discount, Product
from .validators import CountValidator, DiscountCodeValidator

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
    total_price = models.PositiveBigIntegerField(default=0, verbose_name=_("Total Price"),
        help_text=_("Total Price is Sum of Pure Price of Product Items for this Order"))
    final_price = models.PositiveBigIntegerField(default=0, verbose_name=_("Final Price"),
        help_text=_("Final Price is Sum of Price of Product Items for this Order After Dicount"))
    code = models.CharField(max_length=10, default=None, null=True, blank=True,
        verbose_name=_("Discount Code"), help_text=_("If You have a Discount Code Please Enter it"))
    discount = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL,
        related_name='+', default=None, null=True, verbose_name=_("Discount Value"),
        help_text=_("Please Select Discount from Discount Codes to Apply on Price"))

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.__pre_discount = self.discount  # for check changed value in save method

    def update_price(self):
        """
        Update Prices of Order by Change in Items so Calculate Sum Price Again
        """

        self.total_price, self.final_price = 0, 0
        for item in self.items.all():
            self.total_price += item.count * item.product.price
            self.final_price += item.count * item.product.final_price
        if self.discount is not None:
            self.final_price = self.discount.calculate_price(self.final_price)
        self.save()

    def clean(self):
        if self.code is not None:
            discode = DiscountCode.objects.filter(code__exact=self.code)
            if self.discount is None:
                DiscountCodeValidator(discode)(self.customer)
            self.discount = discode[0]
        elif self.__pre_discount is not None:
            self.discount = None

    def save(self, *args, **kwargs):
        if self.discount != self.__pre_discount:
            if self.__pre_discount is not None:
                self.__pre_discount.users.remove(self.customer)
            if self.discount is not None:
                self.discount.users.add(self.customer)
            self.__pre_discount = self.discount
            self.update_price()
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
    count = models.PositiveIntegerField(default=1, verbose_name=_("Count of Order Item"),
        help_text=_("Please Selcet the Count of this Order Item(Minimum Value is 1)."))

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        if self.id is not None:
            self.__pre_count = self.count  # for compare with old value & update inventory
        else:
            self.__pre_count = 0

    def clean(self):
        CountValidator(self.product)(self.count - self.__pre_count)
    
    def save(self, *args, **kwargs):
        if self.order.status == 'U':
            if self.id is None:
                self.product.inventory -= self.count
                self.product.save()
            elif self.count != self.__pre_count:
                self.product.inventory -= (self.count - self.__pre_count)
                self.product.save()
            result = super(self.__class__, self).save(*args, **kwargs)
            self.order.update_price()
            return result

    def __str__(self) -> str:
        return f"{self.order.id} - {self.product.title} - {self.count}"
