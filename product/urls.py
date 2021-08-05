from django.urls import path

from .views import *

app_name = "product"
urlpatterns = [
    path('', ProductsListView.as_view(), name="lists"),
    path('category/', CategoryListView.as_view(), name="categories"),
    path('<slug>', ProductDetailView.as_view(), name="details"),
]
