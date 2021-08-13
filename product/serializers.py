from rest_framework import serializers

from .models import *

class BrandBriefSerializer(serializers.ModelSerializer):
    """
    Brief Serializer for Brand Model Show Important Fields
    """

    class Meta:
        model = Brand
        fields = (
            "id", "title_en", "title_fa", "slug"
        )


class BrandSerializer(serializers.ModelSerializer):
    """
    Serializer for Brand Model Show All of the Fields
    """

    products = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Brand
        fields = (
            "id", "title_en", "title_fa", "slug", "logo", "link", "products"
        )


class DiscountBriefSerializer(serializers.ModelSerializer):
    """
    Brief Serializer for Discount Model Show Important Fields
    """

    class Meta:
        model = Discount
        fields = (
            "id", "title_en", "title_fa", "slug", "unit", "amount", "roof"
        )


class DiscountSerializer(serializers.ModelSerializer):
    """
    Serializer for Discount Model Show All of the Fields
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
    brand = serializers.HyperlinkedRelatedField(view_name="api:brand_detail",
        read_only=True, lookup_field='slug', lookup_url_kwarg='name')

    class Meta:
        model = Product
        fields = (
            "id", "title_en", "title_fa", "slug", "category", "brand", "price"
        )


class ProductSerializer(serializers.ModelSerializer):
    """
    Show Full Information and Fields of Products for Use in Detail Page
    """

    category = serializers.HyperlinkedRelatedField(view_name="api:category_detail",
        read_only=True, lookup_field='slug', lookup_url_kwarg='name')
    brand = serializers.HyperlinkedRelatedField(view_name="api:brand_detail",
        read_only=True, lookup_field='slug', lookup_url_kwarg='name')
    properties = serializers.ReadOnlyField(source='property_dict')

    class Meta:
        model = Product
        fields = (
            "id", "title_en", "title_fa", "slug", "category", "brand", "price",
            "inventory", "image", "discount", "properties"
        )
