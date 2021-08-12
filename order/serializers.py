from rest_framework import serializers

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
    Serializer for Discount Model Show All of the Fields
    """

    users = serializers.HyperlinkedRelatedField(view_name="api:customer_detail",
        read_only=True, many=True, lookup_field='username', lookup_url_kwarg='phone')

    class Meta:
        model = DiscountCode
        fields = (
            "id", "code", "title_en", "title_fa", "slug",
            "unit", "amount", "roof", "start_date", "end_date", "users"
        )
