from django.contrib import admin

from .models import Message

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Message Admin Class to Show Received Message for Admin in Panel with Info
    """

    fields = (('first_name', 'last_name'), ('phone_number', 'email'), 'text')
    list_display = ('phone_number', 'first_name', 'last_name', 'email')
    list_filter = ('create_timestamp',)
    search_fields = ('text', 'first_name', 'last_name', 'phone_number', 'email')
    ordering = ('-create_timestamp',)

    # staff admin can't anything edit on messages add change or delete just see
    def has_add_permission(self, request) -> bool:
        return False
    
    def has_change_permission(self, request, obj=None) -> bool:
        return False
    
    def has_delete_permission(self, request, obj=None) -> bool:
        return False
