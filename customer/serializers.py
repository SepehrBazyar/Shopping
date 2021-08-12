from rest_framework import serializers

from .models import *

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

    class Meta:
        model = Customer
        fields = (
            "id", "username", "first_name", "last_name", "phone_number", "email",
            "staff", "gender", "birth_day", "photo"
        )
