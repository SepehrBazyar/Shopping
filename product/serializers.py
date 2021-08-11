from rest_framework import serializers

from .models import *

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = (
            "id", "title_en", "title_fa", "slug",
            "unit", "amount", "roof", "start_date", "end_date"
        )
