from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import serializers

from rookly.authentication.models import User
from ..city.serializers import CitySerializer
from ..fields import PasswordField


class LoginSerializer(AuthTokenSerializer, serializers.ModelSerializer):
    username = serializers.EmailField(label=_("Email"))
    password = PasswordField(label=_("Password"))

    class Meta:
        model = User
        fields = ["username", "password"]
        ref_name = None


class RegisterUserSerializer(serializers.ModelSerializer):
    password = PasswordField(
        write_only=True, validators=[validate_password], label=_("Password")
    )

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "cpf",
            "password",
            "telephone",
            "address_cep",
            "address_number",
            "address_complement",
            "birth_date",
        ]
        ref_name = None

    @staticmethod
    def validate_password(value):
        return make_password(value)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "telephone",
            "business",
            "city",
        ]
        ref_name = None

    business = serializers.SerializerMethodField()
    city = CitySerializer(many=False)

    def get_business(self, obj):
        return obj.business.all().exists()
