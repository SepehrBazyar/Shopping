from django.shortcuts import render

from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.permissions import *
from order.serializers import *

# Create your views here.
class DiscountCodeListAPIView(generics.ListCreateAPIView):
    """
    View for See List of Discount Code & Create New if User is Staff
    """

    serializer_class = DiscountCodeBriefSerializer
    queryset = DiscountCode.objects.all()
    permission_classes = [
        IsOwnerSite
    ]


class DiscountCodeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for See Details of a Discount Code by Code Field for Staff Users
    """

    serializer_class = DiscountCodeSerializer
    queryset = DiscountCode.objects.all()
    lookup_field = 'code'
    lookup_url_kwarg = 'code'
    permission_classes = [
        IsOwnerSite
    ]


class OrderListAPIView(viewsets.ModelViewSet):
    """
    View for See List of Orders Just if User is Staff
    """

    serializer_class = OrderBriefSerializer
    queryset = Order.objects.all()
    permission_classes = [
        IsStaffAuthenticated
    ]

    def get_queryset(self):
        user = self.request.user
        result = super().get_queryset()
        if not user.is_staff:
            result = result.filter(customer__username=user.username)
        return result


class OrderDetailAPIView(viewsets.ModelViewSet):
    """
    View for See Details of a Order by Recepite Number Just is Onwer or Staff
    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'number'
    permission_classes = [
        IsOwnerUser
    ]


class OrderItemListAPIView(viewsets.ModelViewSet):
    """
    View for See List of Order Items Just if User is Staff
    """

    serializer_class = OrderItemBriefSerializer
    queryset = OrderItem.objects.all()
    permission_classes = [
        IsOwnerSite
    ]


class OrderItemDetailAPIView(viewsets.ModelViewSet):
    """
    View for See Details of a Order Item Just User is Onwer of Order or is Staff
    """

    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'number'
    permission_classes = [
        IsCustomerOwnerParent
    ]
