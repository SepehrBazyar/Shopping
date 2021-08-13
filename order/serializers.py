from rest_framework import serializers

from product.serializers import *
from customer.serializers import *
from .models import *

class DiscountCodeBriefSerializer(serializers.ModelSerializer):
    """
    Brief Serializer for Discount Code Model Show Important Fields
    """

    class Meta:
        model = DiscountCode
        fields = (
            "id", "code", "title_en", "title_fa", "slug", "unit", "amount", "roof"
        )


class DiscountCodeSerializer(serializers.ModelSerializer):
    """
    Serializer for Discount Code Model Show All of the Fields
    """

    users = serializers.HyperlinkedRelatedField(view_name="api:customer_detail",
        read_only=True, many=True, lookup_field='username', lookup_url_kwarg='phone')

    class Meta:
        model = DiscountCode
        fields = (
            "id", "code", "title_en", "title_fa", "slug",
            "unit", "amount", "roof", "start_date", "end_date", "users"
        )


class OrderItemBriefSerializer(serializers.ModelSerializer):
    """
    Brief Serializer for Order Item Model Show Important Fields
    """

    class Meta:
        model = OrderItem
        fields = (
            "id", "product", "count"
        )


# class OrderItemSerializer(serializers.ModelSerializer):
#     """
#     Serializer for Order Item Model Show All of the Fields
#     """

#     class Meta:
#         model = OrderItem
#         fields = (
#             "id", "status", "customer", "address",
#             "total_price", "final_price", "discount", "items"
#         )


class OrderBriefSerializer(serializers.ModelSerializer):
    """
    Brief Serializer for Order Model Show Important Fields
    """

    customer = serializers.HyperlinkedRelatedField(view_name="api:customer_detail",
        read_only=True, lookup_field='username', lookup_url_kwarg='phone')

    class Meta:
        model = Order
        fields = (
            "id", "status", "customer", "total_price", "final_price"
        )


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order Model Show All of the Fields
    """

    items = OrderItemBriefSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = (
            "id", "status", "customer", "address",
            "total_price", "final_price", "discount", "items"
        )
