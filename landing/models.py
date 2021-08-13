from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _

from core.models import BasicModel
from core.validators import Validators

# Create your models here.
class Message(BasicModel):
    """
    Message Model for Create Contact Form and Show Messages in Admin Panel
    """

    class Meta:
        verbose_name, verbose_name_plural = _("Message"), _("Messages")

    first_name = models.CharField(max_length=100, verbose_name=_("First Name"), 
        help_text=_("Please Enter Your First Name."))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"), 
        help_text=_("Please Enter Your Last Name."))
    phone_number = models.CharField(max_length=11, verbose_name=_("Phone Number"),
        validators=[Validators.check_phone_number], help_text=_("Please Enter Your Phone Number"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email Address"),
        help_text=_("Please Enter Your Email Address(Optional)."))
    text = models.TextField(verbose_name=_("Message Text"),
        help_text=_("Please Write Your Message Text..."))

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
