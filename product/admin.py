from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.admin import *
from .models import *

# Register your models here.
class BasicTabularInline(admin.TabularInline):
    """
    Basic Tabular Model Admin for Inheritance All Other Models
    """

    fields = [('title_fa', 'title_en', 'slug')]
    exclude = ['deleted', 'delete_timestamp']
    prepopulated_fields = {
        'slug': ('title_en',),
    }
    extra = 1


class BasicStackedInline(admin.StackedInline):
    """
    Basic Stacked Model Admin for Inheritance All Other Models
    """

    fields = ['title_fa', 'title_en', 'slug']
    exclude = ['deleted', 'delete_timestamp']
    prepopulated_fields = {
        'slug': ('title_en',),
    }
    extra = 1


class CategoryInline(BasicTabularInline):
    """
    Create New Category Instance in Category Admin Page with Tabular Inline Model
    """

    model = Category
    exclude = BasicTabularInline.exclude + ['properties']
    verbose_name_plural = _("Subcategories")


class ProductInline(BasicStackedInline):
    """
    Create New Product Instance in Brand Admin Page with Stacked Inline Model
    """

    model = Product
    exclude = BasicStackedInline.exclude + ['properties']
    verbose_name_plural = _("Manufactured Products")
    fields = BasicTabularInline.fields + [
        'category',
        ('image', 'inventory'),
        ('price', 'discount')
    ]


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

    exclude = TranslateAdmin.exclude + ['properties']
    fieldsets = TranslateAdmin.fieldsets + [
        (_("Optional Information"), {
            'fields': ('root',),
        }),
    ]
    list_display = TranslateAdmin.list_display + ['root']
    inlines = [CategoryInline]


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
    inlines = [ProductInline]


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
            'classes': ('collapse',),
            'fields': [('start_date', 'end_date')],
        }),
    ]
    list_display = TranslateAdmin.list_display + ['start_date', 'end_date']
    list_filter = ['unit', 'start_date', 'end_date']
    actions = ['beginning', 'finishing']

    @admin.action(description=_("Beginning Selected Discount"))
    def beginning(self, request, queryset):
        """
        Action for Change Start Date of Selected Discount to Now
        """

        updated = queryset.update(start_date=timezone.now())
        if updated == 1:
            message = _(" Discount was Successfully Beginning.")
        else:
            message = _(" Discounts were Successfully Beginning.")
        self.message_user(request, str(updated) + message)

    @admin.action(description=_("Finishing Selected Discount"))
    def finishing(self, request, queryset):
        """
        Action for Change End Date of Selected Discount to Now
        """

        updated = queryset.update(end_date=timezone.now())
        if updated == 1:
            message = _(" Discount was Successfully Finishing.")
        else:
            message = _(" Discounts were Successfully Finishing.")
        self.message_user(request, str(updated) + message)


@admin.register(Product)
class ProductAdmin(TranslateAdmin):
    """
    Manage Product Item Class Model and Show Fields in Panel Admin
    """

    exclude = TranslateAdmin.exclude + ['properties']
    fieldsets = TranslateAdmin.fieldsets + [
        (_("Further information"), {
            'fields': (
                ('image', 'inventory'),
                ('category', 'brand'),
                ('price', 'discount'),
            ),
        }),
    ]
    list_display = TranslateAdmin.list_display + \
        ['category', 'brand', 'price', 'discount', 'final_price']
    list_filter = ('category', 'brand', 'discount')
    list_editable = ['price']
