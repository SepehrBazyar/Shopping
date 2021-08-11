from rest_framework import serializers

from .models import *

class DiscountSerializer(serializers.ModelSerializer):
    """
    Serializer for Discount Model Show Important Fields
    """

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
    root = CategoryBriefSerializer(read_only=True)
    subcategories = CategoryBriefSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = (
            "id", "title_en", "title_fa", "slug", "root", "properties", "subcategories"
        )


class ProductBriefSerializer(serializers.ModelSerializer):
    """
    Show Breif Information of Product for Show in List Page
    """

    category = serializers.HyperlinkedRelatedField(view_name="api:category_detail",
        read_only=True, lookup_field='slug', lookup_url_kwarg='name')

    class Meta:
        model = Product
        fields = (
            "id", "title_en", "title_fa", "slug", "category", "price"
        )


class ProductSerializer(serializers.ModelSerializer):
    """
    Show Full Information and Fields of Products for Use in Detail Page
    """

    category = serializers.HyperlinkedRelatedField(view_name="api:category_detail",
        read_only=True, lookup_field='slug', lookup_url_kwarg='name')
    properties = serializers.ReadOnlyField(source='property_dict')

    class Meta:
        model = Product
        fields = (
            "id", "title_en", "title_fa", "slug", "category", "price",
            "inventory", "image", "discount", "properties"
        )
