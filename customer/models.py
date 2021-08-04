from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BasicModel, User
from core.validators import Validators

# Create your models here.
class Customer(User):
    """
    Customer Model is Like User But Can't Enter Admin Panel.\n
    Customer Just Can See Products and Categories and Create New Orders.
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Customer"), _("Customers")

    GENDERS = {
        'M': _("Male"),
        'F': _("Female"),
        'N': _("Non-Binary"),
    }

    photo = models.FileField(upload_to="customer/customers/", verbose_name=_("Profile Picture"),
        default="Unknown.jpg", blank=True, help_text=_("Please Upload Uour Image if You Wish."))
    gender = models.CharField(max_length=1, default=None, null=True, blank=True,
        choices=[(key, value) for key, value in GENDERS.items()],
        verbose_name=_("Gender"), help_text=_("Please Select Your Gender if You Wish."))
    birth_day = models.DateField(default=None, null=True, blank=True,
        verbose_name=_("Birth Day"), help_text=_("Please Enter Your Birth Day if You Wish."))

    def delete(self):
        self.is_active = False
        self.save()


class Address(BasicModel):
    """
    Address Model Includes Country, Province & City and belongs to Customers
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Address"), _("Addresses")

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses",
        verbose_name=_("Customer"), help_text=_("Please Select Customer Owner this Address"))
    postal_code = models.CharField(max_length=10, unique=True, verbose_name=_("Postal Code"),
        validators=[Validators.check_postal_code], help_text=_("Please Enter Your Postal Code"))
    country = models.CharField(max_length=10, default="ایران", verbose_name=_("Country"),
        help_text=_("Please Enter Your Country(By Default Iran is Considered)."))
    province = models.CharField(max_length=10,  verbose_name=_("Province"),
        help_text=_("Please Enter Your Province For Example Tehran or Alborz or ..."))
    city = models.CharField(max_length=10,  verbose_name=_("City"),
        help_text=_("Please Enter Your City For Example Tehran or Karaj or ..."))
    rest = models.TextField(verbose_name=_("Continue Address(Street and Alley)"),
                            help_text=_("Please Enter the Rest of Your Address Accurately"))

    def __str__(self) -> str:
        return f"{self.city}({self.province}) - {self.postal_code}"
