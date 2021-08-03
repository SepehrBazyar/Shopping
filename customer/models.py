from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import User

# Create your models here.
class Cutomer(User):
    """
    Customer Model is Like User But Can't Enter Admin Panel.\n
    Customer Just Can See Products and Categories and Create New Orders.
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Customer"), _("Cutomers")

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
    birth_date = models.DateField(default=None, null=True, blank=True,
        verbose_name=_("Birth Day"), help_text=_("Please Enter Your Birth Day if You Wish."))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_staff = False
    
    def delete(self):
        self.is_active = False
        self.save()

    def __str__(self) -> str:
        return super().__str__()

class Address:
    pass
