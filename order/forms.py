from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *
from .validators import *

class OrderItemForm(forms.ModelForm):
    """
    Form by Order Item Model to Change Count and Check Available Inventory
    """

    class Meta:
        model = OrderItem
        exclude = ['deleted', 'delete_timestamp']
        widgets = {
            'order': forms.HiddenInput(),
            'product': forms.HiddenInput(),
        }


class OrderForm(forms.ModelForm):
    """
    Create Form by Order Model Just Get Code for Check Discount Code
    """

    class Meta:
        model = Order
        exclude = ['deleted', 'delete_timestamp', 'address']
        widgets = {
            'status': forms.HiddenInput(),
            'customer': forms.HiddenInput(),
            'total_price': forms.HiddenInput(),
            'final_price': forms.HiddenInput(),
            'discount': forms.HiddenInput(),
        }
