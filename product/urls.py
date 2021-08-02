from django.urls import path

from .views import *

app_name = "product"
urlpatterns = [
    path('', ProductsListView.as_view(), name="lists"),
    path('<slug>', ProductDetailView.as_view(), name="details"),
]
