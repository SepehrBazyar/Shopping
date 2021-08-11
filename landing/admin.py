from django.contrib import admin

from .models import Message

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Message Admin Class to Show Received Message for Admin in Panel with Info
    """

    fields = (('first_name', 'last_name'), ('phone_number', 'email'), 'text')
    list_display = ('text', 'first_name', 'last_name', 'phone_number', 'email')
    list_filter = ('create_timestamp',)
    search_fields = ('text', 'first_name', 'last_name', 'phone_number', 'email')
    ordering = ('-create_timestamp',)
