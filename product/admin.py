from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin import *
from .models import *

# Register your models here.
class TranslateAdmin(BasicAdmin):
    """
    Tranlation Admin Class to Fix Titles & Slug in All Inheritanced Class
    """

    fieldsets = [
        (_("Detail Information"), {
            'fields': ('title_fa', ('title_en', 'slug')),
        }),
    ]
    list_display = ['__str__', 'title_en', 'title_fa']
    ordering = ['id']
    prepopulated_fields = {
        'slug': ('title_en',),
    }


@admin.register(Category)
class CategoryAdmin(TranslateAdmin):
    """
    Manage Category Class Model and Show Fields in Panel Admin
    """

    fieldsets = TranslateAdmin.fieldsets + [
        (_("Optional Information"), {
            'fields': ('root',),
        }),
    ]
    list_display = TranslateAdmin.list_display + ['root']


@admin.register(Brand)
class BrandAdmin(TranslateAdmin):
    """
    Manage Brand Class Model and Show Fields in Panel Admin
    """

    fieldsets = TranslateAdmin.fieldsets + [
        (_("Optional Information"), {
            'fields': ('logo', 'link'),
        }),
    ]
    list_display = TranslateAdmin.list_display + ['link']


@admin.register(Discount)
class DiscountAdmin(TranslateAdmin):
    """
    Manage Discount Class Model and Show Fields in Panel Admin
    """

    fieldsets = TranslateAdmin.fieldsets + [
        (_("Value Information"), {
            'fields': [('unit', 'amount', 'roof')],
        }),
        (_("Date Information"), {
            'fields': [('start_date', 'end_date')],
        }),
    ]
    list_display = TranslateAdmin.list_display + ['start_date', 'end_date']
