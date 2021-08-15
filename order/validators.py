from django.core.exceptions import *
from django.utils.translation import gettext_lazy as _

class CountValidator:
    """
    Validator Callable Class for Check Count Order Item Available Product Inventory
    """

    def __init__(self, product_item):
        self.product_item = product_item

    def __call__(self, count: int):
        if count > self.product_item.inventory:
            raise ValidationError(_("The Product Item Inventory isn't Enough!"))


class DiscountCodeValidator:
    """
    Validator Callable Class for Check Validate & Usable Discount Code for Customer
    """

    def __init__(self, discount_code):
        self.discount_code = discount_code

    def __call__(self, customer):
        if self.discount_code.count() > 0:
            if customer in self.discount_code[0].users.all():
                raise ValidationError(_("This Discount Code has been Expired for You!"))
        else:
            raise ValidationError(_("Not Found Any Matching Discount Code!"))


class CustomerAddressValidator:
    """
    Validator Callable Class for Check Owner of Address is Customer of Order
    """

    def __init__(self, customer):
        self.customer = customer
    
    def __call__(self, address):
        if address.customer != self.customer:
            raise ValidationError(_("Owner of Address & Order Must be One Person"))
