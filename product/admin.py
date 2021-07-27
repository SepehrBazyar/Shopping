from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title_en', 'title_fa', 'root']
    ordering = ['id']
