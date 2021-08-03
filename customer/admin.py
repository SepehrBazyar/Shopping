from django.contrib import admin

from core.admin import MyUserAdmin
from .models import *

# Register your models here.
admin.site.register(Cutomer,MyUserAdmin)
