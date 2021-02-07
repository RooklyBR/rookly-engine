from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from rookly.api.v1.account.serializers import UserSerializer
from rookly.api.v1.business.validators import (
    CPFCNPJValidator,
    CanContributeBusinessValidator,
)
from rookly.api.v1.fields import TextField
from rookly.common.models import (
    Business,
    BusinessCategory,
    BusinessService,
    SubCategory,
    City,
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
            "name",
            "cpf_cnpj",
            "city",
            "state",
            "presentation",
            "type_user",
            "created_at",
            "business_category",
        ]
        read_only = ["uuid", "created_at"]
        ref_name = None

    uuid = serializers.UUIDField(style={"show": False}, read_only=True)
    cpf_cnpj = TextField(
        label=_("CPF or CNPJ"),
        min_length=11,
        max_length=Business._meta.get_field("cpf_cnpj").max_length,
        validators=[CPFCNPJValidator()],
        write_only=True,
    )
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects, required=True)
    state = serializers.IntegerField(source="city.state.id", read_only=True)

    type_user = serializers.ChoiceField(
        choices=Business.TYPE_USER_CHOICES,
        default=Business.FREELANCER,
        label=_("Type User"),
    )
    business_category = BusinessCategorySerializer(many=True, read_only=True)

    def create(self, validated_data):
        validated_data.update({"user": self.context["request"].user})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("cpf_cnpj")
        return super().update(instance, validated_data)


class BusinessServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessService
        fields = [
            "id",
            "business_control",
            "business",
            "price",
            "payment_type",
            "business_category",
            "user",
            "created_at",
        ]
        read_only = ["id", "created_at"]
        ref_name = None

    business_control = BusinessSerializer(many=False, read_only=True, source="business")
    business = serializers.PrimaryKeyRelatedField(
        queryset=Business.objects,
        help_text=_("Business UUID"),
        required=True,
        write_only=True,
        validators=[CanContributeBusinessValidator()],
    )
    business_category = BusinessCategorySerializer(many=False)
    payment_type = serializers.ChoiceField(
        choices=BusinessService.TYPE_PAYMENT_CHOICES,
        default=BusinessService.PAYMENT_HOUR,
        label=_("Payment Type"),
    )
    user = UserSerializer(many=False, source="business.user", read_only=True)

    def create(self, validated_data):
        business = validated_data.get("business")
        business_category = business.business_category.create(
            subcategory=validated_data.get("business_category", {}).get("subcategory"),
        )
        validated_data.update({"business_category": business_category})
        business_service = super().create(validated_data)
        return business_service

    def update(self, instance, validated_data):
        # validated_data.pop("user")
        validated_data.pop("business")
        return super().update(instance, validated_data)
