from django.urls import path

from .views import *

app_name = "order"
urlpatterns = [
    path('cart/', BasketCartView.as_view(), name="cart"),
    path('items/', ChangeItemView.as_view(), name="count"),
    path('orders/', OrdersCustomerView.as_view(), name="orders"),
    path('change/', ChangeCartStatusView.as_view(), name="change"),
    path('remove/', RemoveItemView.as_view(), name="remove")
]
