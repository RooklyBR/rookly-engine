from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from rookly.api.v1.business.validators import CPFCNPJValidator
from rookly.api.v1.fields import TextField
from rookly.common.models import (
    Business,
    BusinessCategory,
    BusinessService,
    SubCategory,
)


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = ["id", "subcategory"]
        ref_name = None

    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects, style={"show": False}, required=True
    )


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            "uuid",
            "cpf_cnpj",
            "presentation",
            "type_user",
            "created_at",
        ]
        read_only = ["uuid", "created_at"]
        ref_name = None

    uuid = serializers.UUIDField(style={"show": False}, read_only=True)
    cpf_cnpj = TextField(
        label=_("CPF or CNPJ"),
        min_length=11,
        max_length=Business._meta.get_field("cpf_cnpj").max_length,
        validators=[CPFCNPJValidator()],
    )

    type_user = serializers.ChoiceField(
        choices=Business.TYPE_USER_CHOICES,
        default=Business.FREELANCER,
        label=_("Type User"),
    )

    def create(self, validated_data):
        validated_data.update({"user": self.context["request"].user})
        return super().create(validated_data)


class BusinessServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessService
        fields = [
            "id",
            "business",
            "price_hours",
            "business_category",
            "created_at",
        ]
        read_only = ["id", "created_at"]
        ref_name = None

    business = serializers.PrimaryKeyRelatedField(
        queryset=Business.objects, style={"show": False}, required=True
    )
    business_category = BusinessCategorySerializer(many=False)

    def create(self, validated_data):
        business = validated_data.get("business")
        business_category = business.business_category.create(
            subcategory=validated_data.get("business_category", {}).get("subcategory"),
        )
        validated_data.update({"business_category": business_category})
        business_service = super().create(validated_data)
        return business_service
