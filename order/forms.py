from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *
from .validators import *

class OrderItemForm(forms.ModelForm):
    """
    
    """

    class Meta:
        model = OrderItem
        fields = ('product', 'count')


class OrderForm(forms.ModelForm):
    """
    Create Form by Order Model Just Get Code for Check Discount Code
    """

    class Meta:
        model = Order
        exclude = ['deleted', 'delete_timestamp']
        widgets = {
            'status': forms.HiddenInput(),
            'customer': forms.HiddenInput(),
            'total_price': forms.HiddenInput(),
            'final_price': forms.HiddenInput(),
            'discount': forms.HiddenInput(),
        }
