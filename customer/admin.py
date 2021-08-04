from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin import MyUserAdmin
from .models import *

# Register your models here.
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
