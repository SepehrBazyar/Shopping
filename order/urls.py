from django.urls import path

from .views import *

app_name = "order"
urlpatterns = [
    path('cart/', BasketCartView.as_view(), name="cart"),
    path('orders/', OrdersCustomerView.as_view(), name="orders")
]
