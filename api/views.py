from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from product.serializers import *

# Create your views here.
@api_view(['GET'])
def first(request):
    if request.method == 'GET':
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data)
