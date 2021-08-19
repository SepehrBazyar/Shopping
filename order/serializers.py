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
            "id", "order", "product", "count"
        )
        extra_kwargs = {
            'order': {
                "write_only": True,
            },
        }



class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Order Item Model Show All of the Fields
    """

    order = serializers.HyperlinkedRelatedField(view_name="api:order_detail",
        read_only=True, lookup_field='id', lookup_url_kwarg='number')

    class Meta:
        model = OrderItem
        fields = (
            "id", "order", "product", "count"
        )


class OrderBriefSerializer(serializers.ModelSerializer):
    """
    Brief Serializer for Order Model Show Important Fields
    """

    owner = serializers.HyperlinkedRelatedField(view_name="api:customer_detail",
        read_only=True, lookup_field='username', lookup_url_kwarg='phone', source="customer")

    class Meta:
        model = Order
        fields = (
            "id", "status", "owner", "customer", "address",
            "total_price", "final_price", "code", "discount"
        )
        extra_kwargs = {
            'customer': {
                "write_only": True,
            },
            'address': {
                "write_only": True,
            },
            'code': {
                "write_only": True,
            },
            'discount': {
                "write_only": True,
            },
        }


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order Model Show All of the Fields
    """

    customer = CustomerBriefSerializer(read_only=True)
    address = serializers.HyperlinkedRelatedField(view_name="api:address_detail",
        read_only=True, lookup_field='zip_code', lookup_url_kwarg='code')
    discount = DiscountCodeBriefSerializer(read_only=True)
    items = OrderItemBriefSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = (
            "id", "status", "customer", "address",
            "total_price", "final_price", "code", "discount", "items"
        )
