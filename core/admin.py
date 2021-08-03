from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.
admin.site.register(User, UserAdmin)

class BasicAdmin(admin.ModelAdmin):
    """
    Excluded logical Delete Fields for All Model in Panel Admin
    """

    exclude = ['deleted', 'delete_timestamp']
    search_fields = ['title_en', 'title_fa']
