from rest_framework import serializers

from .models import *

class AddressBriefSerializer(serializers.ModelSerializer):
    """
    Brief Serializer for Address Model Show Important Fields
    """

    class Meta:
        model = Address
        fields = (
            "id", "customer", "zip_code", "name", "lat", "lng",
            "country", "province", "city", "rest"
        )
        extra_kwargs = {
            'customer': {
                "write_only": True,
            },
            'country': {
                "write_only": True,
            },
            'province': {
                "write_only": True,
            },
            'city': {
                "write_only": True,
            },
            'rest': {
                "write_only": True,
            },
        }


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for Address Model Show All of the Fields
    """

    customer = serializers.HyperlinkedRelatedField(view_name="api:customer_detail",
        read_only=True, lookup_field='username', lookup_url_kwarg='phone')

    class Meta:
        model = Address
        fields = (
            "id", "customer", "zip_code", "name", "lat", "lng",
            "country", "province", "city", "rest"
        )


class CustomerBriefSerializer(serializers.ModelSerializer):
    """
    Brief Serializer for Customer Model Show Important Fields
    """

    class Meta:
        model = Customer
        fields = (
            "id", "username", "first_name", "last_name", "phone_number", "email"
        )


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer Model Show All of the Fields
    """

    staff = serializers.ReadOnlyField(source='is_staff')
    addresses = AddressBriefSerializer(read_only=True, many=True)
    codes = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    orders = serializers.HyperlinkedRelatedField(view_name="api:order_detail",
        many=True, read_only=True, lookup_field='id', lookup_url_kwarg='number')

    class Meta:
        model = Customer
        fields = (
            "id", "username", "first_name", "last_name", "phone_number", "email",
            "staff", "gender", "birth_day", "photo", "addresses", "codes", "orders"
        )
