from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from .models import *

class CustomerForm(UserCreationForm):
    """
    Created Form for Register New Customers by Model Fields
    """

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': _("Phone Number"),
        }
        help_texts = {
            'username': _("Please Enter Your Phone Number")
        }
