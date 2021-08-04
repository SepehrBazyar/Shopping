from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BasicModel
from customer.models import Customer
from product.models import Discount, Product

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
    code = models.CharField(max_length=10, default=None, null=True, verbose_name=_("Discount Code"),
        help_text=_("If You have a Discount Cod Please Enter it to Apply on Order Price"))
    discount = models.ForeignKey(DiscountCode, related_name='+', default=None, null=True,
        verbose_name=_("Discount Value"), help_text=_("Please Select Discount from Discount Codes"))

    def clean(self) -> None:
        return super().clean()

    def __str__(self) -> str:
        return super().__str__()


class OrderItem(BasicModel):
    """
    Model of Order Items for Connect to Recepite Order & Product Items
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Order Item"), _("Order Items")



    def clean(self) -> None:
        return super().clean()
    
    def __str__(self) -> str:
        return super().__str__()
