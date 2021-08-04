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
            raise ValidationError(_("Inventory of Product Item isn't Enough!"))
        self.product_item.inventory -= count
        self.product_item.save()


class DiscountCodeValidator:
    """
    Validator Callable Class for Check Validate & Usable Discount Code for Customer
    """

    def __init__(self, discount_code):
        self.discount_code = discount_code

    def __call__(self, customer):
        if self.discount_code.count() > 0:
            if customer in self.discount_code[0].users.all():
                raise ValidationError(_("This Discount Code has Expired for You!"))
            else:
                self.discount_code[0].users.add(customer)
        else:
            raise ValidationError(_("Not Found Matching Any Discount Code!"))
