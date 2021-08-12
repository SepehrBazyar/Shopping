from api.views.view_customer import CustomerDetailAPIView, CustomerListAPIView
from django.urls import path

from .views.view_product import *

app_name = "api"
urlpatterns = [
    # product app
    path('product/brand/', BrandListAPIView.as_view(), name="brand_list"),
    path('product/brand/<str:name>/', BrandDetailAPIView.as_view(), name="brand_detail"),
    path('product/discount/', DiscountListAPIView.as_view(), name="discount_list"),
    path('product/discount/<str:name>/', DiscountDetailAPIView.as_view(), name="discount_detail"),
    path('product/category/', CategoryListAPIView.as_view(), name="category_list"),
    path('product/category/<str:name>/', CategoryDetailAPIView.as_view(), name="category_detail"),
    path('product/product/', ProductListAPIView.as_view(), name="product_list"),
    path('product/product/<str:name>/', ProductDetailAPIView.as_view(), name="product_detail"),

    # customer app
    path('customer/customer/', CustomerListAPIView.as_view(), name="customer_list"),
    path('customer/customer/<str:phone>/', CustomerDetailAPIView.as_view(), name="customer_detail"),

    # order app


]
