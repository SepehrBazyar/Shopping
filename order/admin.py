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

    @admin.action(description=_("Beginning Selected Discount Codes"))
    def beginning(self, request, queryset):
        """
        Action for Change Start Date of Selected Discount Codes to Now
        """

        updated = queryset.update(start_date=timezone.now())
        if updated == 1:
            message = _(" Discount Code was Successfully Beginning.")
        else:
            message = _(" Discount Codes were Successfully Beginning.")
        self.message_user(request, str(updated) + message)

    @admin.action(description=_("Finishing Selected Discount Codes"))
    def finishing(self, request, queryset):
        """
        Action for Change End Date of Selected Discount Codes to Now
        """

        updated = queryset.update(end_date=timezone.now())
        if updated == 1:
            message = _(" Discount Code was Successfully Finishing.")
        else:
            message = _(" Discount Codes were Successfully Finishing.")
        self.message_user(request, str(updated) + message)


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
    readonly_fields = ['total_price', 'final_price']
    list_display = ('__str__', 'customer', 'total_price', 'final_price', 'status', 'discount')
    list_filter = ('status',)
    search_fields = ('customer',)
    ordering = ('-id',)
    inlines = [OrderItemInlineAdmin]
    actions = ['paymenting', 'canceling']

    @admin.action(description=_("Paymenting Selected Order"))
    def paymenting(self, request, queryset):
        """
        Action for Change Status of Selected Orders to Paid
        """

        updated = queryset.update(status='P')
        if updated == 1:
            message = _(" Order was Successfully Paiding.")
        else:
            message = _(" Orders were Successfully Paiding.")
        self.message_user(request, str(updated) + message)
    
    @admin.action(description=_("Canceling Selected Order"))
    def canceling(self, request, queryset):
        """
        Action for Change Status of Selected Orders to Canceled
        """

        updated = queryset.update(status='C')
        if updated == 1:
            message = _(" Order was Successfully Canceling.")
        else:
            message = _(" Orders were Successfully Canceling.")
        self.message_user(request, str(updated) + message)


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
