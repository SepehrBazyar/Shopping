from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.permissions import *
from customer.serializers import *

# Create your views here.
class CustomerListAPIView(generics.ListAPIView):
    """
    View for See List of Customers Just is Staff User
    """

    serializer_class = CustomerBriefSerializer
    queryset = Customer.objects.all()
    permission_classes = [
        IsOwnerSite
    ]


class CustomerDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    View for See Details of a Customer Just is Owner or Staff User
    """

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    lookup_field = 'username'
    lookup_url_kwarg = 'phone'
    permission_classes = [
        IsCustomerUser
    ]
