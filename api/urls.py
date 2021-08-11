from django.urls import path

from .views import *

app_name = "api"
urlpatterns = [
    path('discount/', DiscountListAPIView.as_view(), name="discount_list"),
    path('discount/<str:name>/', DiscountDetailAPIView.as_view(), name="discount_detail"),
    path('category/', CategoryListAPIView.as_view(), name="category_list"),
    path('category/<str:name>/', CategoryDetailAPIView.as_view(), name="category_detail"),
]
