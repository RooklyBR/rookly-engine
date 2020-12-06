from rest_framework import serializers

from rookly.common.models import (
    SubCategory,
    Category,
)


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name"]
        ref_name = None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "subcategory"]
        ref_name = None

    subcategory = SubCategorySerializer(many=True)
