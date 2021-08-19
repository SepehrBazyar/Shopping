from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from core.permissions import *
from customer.serializers import *

# Create your views here.
class CustomerListAPIView(generics.ListAPIView):
    """
    View for Just See List of Customers Just is Staff User
    """

    serializer_class = CustomerBriefSerializer
    queryset = Customer.objects.all()
    permission_classes = [
        IsOwnerSite
    ]


class CustomerDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    View for See and Edit(not Delete) Details of a Customer Just is Owner or Staff User
    """

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    lookup_field = 'username'
    lookup_url_kwarg = 'phone'
    permission_classes = [
        IsCustomerUser
    ]


class AddressListAPIView(generics.ListCreateAPIView):
    """
    View for Just See List of Addresses Just is Staff User
    """

    serializer_class = AddressBriefSerializer
    queryset = Address.objects.all()
    permission_classes = [
        IsCustomerOwner
    ]

    def get_queryset(self):
        user = self.request.user
        result = super().get_queryset()
        if not user.is_staff:
            result = result.filter(customer__username=user.username)
        return result
    
    def perform_create(self, serializer):
        customer = Customer.objects.get(username=self.request.user.username)
        serializer.save(customer=customer)


class AddressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for See and Edit Details of a Address Just is Owner or Staff User
    """

    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    lookup_field = 'zip_code'
    lookup_url_kwarg = 'code'
    permission_classes = [
        IsOwnerUser
    ]
