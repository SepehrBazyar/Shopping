from rest_framework import serializers

from .models import *

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = (
            "id", "title_en", "title_fa", "slug",
            "unit", "amount", "roof", "start_date", "end_date"
        )


class CategoryBriefSerializer(serializers.ModelSerializer):
    """
    Show Breif Information of Category for Use in Other Models
    """

    class Meta:
        model = Category
        fields = ("id", "title_en", "title_fa", "slug")

class CategorySerializer(serializers.ModelSerializer):
    """
    Show Full Information and Fields of Category for Use in Self
    """

    properties = serializers.ReadOnlyField(source='property_dict')

    class Meta:
        model = Category
        fields = (
            "id", "title_en", "title_fa", "slug", "properties"
        )
        # depth = 2
