from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import *

# Register your models here.
@admin.register(User)
class MyUserAdmin(UserAdmin):
    """
    Customization Admin Pane of User Model for Show Phone Number & Sync with User Name
    """

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class BasicAdmin(admin.ModelAdmin):
    """
    Excluded logical Delete Fields for All Model in Panel Admin
    """

    exclude = ['deleted', 'delete_timestamp']
    search_fields = ['title_en', 'title_fa']
