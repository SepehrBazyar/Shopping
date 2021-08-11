from django.urls import path

from .views import *

app_name = "api"
urlpatterns = [
    # product app
    path('product/discount/', DiscountListAPIView.as_view(), name="discount_list"),
    path('product/discount/<str:name>/', DiscountDetailAPIView.as_view(), name="discount_detail"),
    path('product/category/', CategoryListAPIView.as_view(), name="category_list"),
    path('product/category/<str:name>/', CategoryDetailAPIView.as_view(), name="category_detail"),
    path('product/product/', ProductListAPIView.as_view(), name="product_list"),
    path('product/product/<str:name>/', ProductDetailAPIView.as_view(), name="product_detail"),
]
