from django.urls import path

from .views import *

app_name = "customer"
urlpatterns = [
    path('register/', CustomerRegisterView.as_view(), name="register"),

]
