from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.permissions import *
from product.serializers import *

# Create your views here.
class DiscountListAPIView(generics.ListCreateAPIView):
    """
    View for See List of Discount & Create New if User is Staff
    """

    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
    permission_classes = [
        IsStaffUser
    ]


class DiscountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for See Details of a Discount by Slug Field for Staff Users
    """

    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'name'
    permission_classes = [
        IsStaffUser
    ]


class CategoryListAPIView(generics.ListCreateAPIView):
    """
    Show Breif List Information of All Categories
    """

    serializer_class = CategoryBriefSerializer
    queryset = Category.objects.all()
    permission_classes = [
        IsStaffUser
    ]


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for Show Completely of Informations of a Category
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'name'
    permission_classes = [
        IsStaffUser
    ]


class ProductListAPIView(generics.ListCreateAPIView):
    """
    
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [
        IsStaffUser
    ]
