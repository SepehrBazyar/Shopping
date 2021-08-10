from django.urls import path

from .views import *

app_name = "api"
urlpatterns = [
    path('discounts/', first, name="first")
]
