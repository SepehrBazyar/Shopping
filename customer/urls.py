from os import name
from django.urls import path

from .views import *

app_name = "customer"
urlpatterns = [
    path('register/', CustomerRegisterView.as_view(), name="register"),
    path('login/', CustomerLoginView.as_view(), name="login"),
    path('logout/', CustomerLogoutView.as_view(), name="logout"),
    path('profile/', CustomerProfileView.as_view(), name="profile"),
    path('password/', ChangePasswordView.as_view(), name="password"),
    path('change/', CustomerEditProfileView.as_view(), name="edit"),
    path('address/', CreateNewAddressView.as_view(), name="address"),
    path('address/<str:zip_code>/', EditAddressView.as_view(), name="change"),
]
