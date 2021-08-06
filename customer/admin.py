from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin import BasicAdmin, MyUserAdmin
from .models import *

# Register your models here.
class AddressInline(admin.StackedInline):
    """
    Create New Address Instance in Customer Admin Page with Stacked Inline Model
    """

    model = Address
    exclude = ['deleted', 'delete_timestamp']
    verbose_name_plural = _("Addresses")
    fields = ('name', ('zip_code', 'country'), ('lat', 'lng'), ('province', 'city'), 'rest')
    extra = 1


@admin.register(Customer)
class CustomerAdmin(MyUserAdmin):
    """
    Customization Admin Panel for Show Details of Customer List Informations
    """

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'email')}),
        (_('Extra info'), {
            'classes': ('collapse',),
            'fields': ('photo', ('gender', 'birth_day'))
        }),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff'),
        }),
        (_('Important dates'), {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined')
        }),
    )
    list_display = ('phone_number', 'first_name', 'last_name', 'email', 'is_active')
    list_filter = ('is_active', 'gender')
    inlines = [AddressInline]


@admin.register(Address)
class AddressAdmin(BasicAdmin):
    """
    Manage Address Class Model and Show Fields in Panel Admin
    """

    fieldsets = (
        (None, {
            'fields': ('customer', 'name', ('zip_code', 'country'),
                        ('lat', 'lng'), ('province', 'city'), 'rest')
        }),
    )
    list_display = ('zip_code', 'province', 'city', 'country')
    list_filter = ('country', 'province', 'city')
    search_fields = ('zip_code', 'country', 'province', 'city')
    ordering = ('-id',)
