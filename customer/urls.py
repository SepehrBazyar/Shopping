from django.urls import path

from .views import *

app_name = "customer"
urlpatterns = [
    path('register/', CustomerRegisterView.as_view(), name="register"),
    path('login/', CustomerLoginView.as_view(), name="login"),
    path('logout/', CustomerLogoutView.as_view(), name="logout"),
]