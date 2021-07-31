from django.contrib import admin

from .models import *

# Register your models here.
class BasicAdmin(admin.ModelAdmin):
    """
    Excluded logical Delete Fields for All Model in Panel Admin
    """

    exclude = ('deleted', 'delete_timestamp')
    search_fields = ['title_en', 'title_fa']
