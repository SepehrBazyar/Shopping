from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin import *
from product.admin import DiscountAdmin
from .models import *

# Register your models here.
class OrderItemInlineAdmin(admin.TabularInline):
    """
    Create New Order Item Instance in Order Admin Page with Tabular Inline Model
    """

    model = OrderItem
    fields = [('product', 'count')]
    exclude = ['deleted', 'delete_timestamp']
    verbose_name_plural = _("Order Items")
    extra = 1


@admin.register(DiscountCode)
class DiscountCodeAdmin(DiscountAdmin):
    """
    Manage Discount Code Class Model and Show Fields in Panel Admin
    """

    exclude = DiscountAdmin.exclude + ['users']
    fieldsets = [(None, {'fields': ('code',)}),] + DiscountAdmin.fieldsets
    list_display = DiscountAdmin.list_display + ['code']
    list_filter  = DiscountAdmin.list_filter  + ['code']


@admin.register(Order)
class OrderAdmin(BasicAdmin):
    """
    Manage Order Class Model and Show Fields in Panel Admin
    """

    exclude = BasicAdmin.exclude + ['discount']
    fieldsets = (
        (None, {
            'fields': (('customer', 'status'), ('total_price', 'final_price'), ('code',)),
        }),
    )
    list_display = ('__str__', 'customer', 'total_price', 'final_price', 'status', 'discount')
    list_filter = ('status',)
    search_fields = ('customer',)
    ordering = ('-id',)
    inlines = [OrderItemInlineAdmin]


@admin.register(OrderItem)
class OrderItemAdmin(BasicAdmin):
    """
    Manage Order Items Class Model and Show Fields in Panel Admin
    """

    fieldsets = (
        (None, {
            'fields': (('order'), ('product', 'count'))
        }),
    )
    list_display = ('__str__', 'order', 'product', 'count')
    search_fields = ('order', 'product')
    ordering = ('-id',)
