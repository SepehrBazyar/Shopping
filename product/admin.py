from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ['deleted', 'delete_timestamp']
    list_display = ['__str__', 'title_en', 'title_fa']
    ordering = ['id']
    prepopulated_fields = {
        'slug': ('title_en', ),
    }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    exclude = ['deleted', 'delete_timestamp']
    list_display = ['__str__', 'title_en', 'title_fa', 'link']
    ordering = ['id']
    prepopulated_fields = {
        'slug': ('title_en', ),
    }
