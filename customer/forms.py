from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, \
                AuthenticationForm, PasswordChangeForm

from .models import *

class CustomerRegisterForm(UserCreationForm):
    """
    Created Form for Register New Customers by Model Fields
    """

    class Meta:
        model = Customer
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': _("Phone Number"),
        }
        help_texts = {
            'username': _("Please Enter Your Phone Number")
        }


class CustomerLoginForm(AuthenticationForm):
    """
    Sign In Customer by Enter Phone Number & Password to Order
    """

    class Meta:
        model = Customer
        fields = ('username', 'password')
        labels = {
            'username': _("Phone Number"),
        }
    
    error_messages = {
        'invalid_login': _(
            "Please Enter a Valid Phone Number and Password."
        ),
    }


class CustomerChangePassword(PasswordChangeForm):
    """
    Inheritanced from Built-in Change Password Form
    """

    pass


class CustomerEditProfileForm(forms.ModelForm):
    """
    Model Form for Change Customer Information Optionals
    """

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'photo', 'gender', 'birth_day')
        widgets = {
            'birth_day': forms.DateInput(attrs={'type':'date'}),
        }


class AdderssForm(forms.ModelForm):
    """
    Model Form for Create New Address for Customers
    """

    class Meta:
        model = Address
        exclude = ['deleted', 'delete_timestamp', 'customer']
