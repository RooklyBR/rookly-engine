from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from rookly.api.v1.business.validators import CPFCNPJValidator
from rookly.api.v1.fields import TextField
from rookly.common.models import Business, BusinessCategory


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = ["id", "category", "business"]
        ref_name = None


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
        read_only = ["id", "type_user", "created_at"]
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
