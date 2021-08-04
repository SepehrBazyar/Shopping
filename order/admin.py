from django.contrib import admin

from core.admin import *
from product.admin import DiscountAdmin
from .models import *

# Register your models here.
@admin.register(DiscountCode)
class DiscountCodeAdmin(DiscountAdmin):
    """
    Manage Discount Code Class Model and Show Fields in Panel Admin
    """

    exclude = DiscountAdmin.exclude + ['users']
    fieldsets = [(None, {'fields': ('code',)}),] + DiscountAdmin.fieldsets
    list_display = DiscountAdmin.list_display + ['code']
    list_filter  = DiscountAdmin.list_filter  + ['code']
