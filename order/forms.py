from django import forms
from django.utils.translation import gettext_lazy as _

from .models import *

class OrderItemForm(forms.ModelForm):
    """
    
    """

    class Meta:
        model = OrderItem
        fields = ('product', 'count')


class OrderForm(forms.ModelForm):
    """
    
    """

    class Meta:
        model = Order
        fields = ('code',)
