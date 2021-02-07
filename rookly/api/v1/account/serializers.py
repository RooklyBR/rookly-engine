from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.db.models import Exists, OuterRef
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError

from rookly.authentication.models import User
from rookly.common.models import BusinessService
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
            "have_business",
            "have_service",
            "photo",
            "birth_date",
            "address_cep",
            "address_number",
            "address_complement",
            "telephone",
        ]
        ref_name = None

    business = serializers.SerializerMethodField()
    have_business = serializers.SerializerMethodField()
    have_service = serializers.SerializerMethodField()
    photo = serializers.ImageField(label=_("User photo"), read_only=True)

    def get_business(self, obj):
        from ..business.serializers import BusinessSerializer

        return BusinessSerializer(
            obj.business,
            many=True,
        ).data

    def get_have_business(self, obj):
        return obj.business.all().exists()

    def get_have_service(self, obj):
        queryset = obj.business.annotate(
            have_service=Exists(
                BusinessService.objects.filter(business=OuterRef("uuid"))
            )
        )
        return queryset.filter(have_service=True).exists()


class UserPhotoSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = PasswordField(required=True, label=_("Current Password"))
    password = PasswordField(
        required=True, validators=[validate_password], label=_("New Password")
    )

    class Meta:
        model = User
        fields = ["current_password", "password"]
        ref_name = None

    def validate_current_password(self, value):
        request = self.context.get("request")
        if not request.user.check_password(value):
            raise ValidationError(_("Wrong password"))
        return value


class RequestResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label=_("Email"), required=True)

    class Meta:
        model = User
        fields = ["email"]
        ref_name = None

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
            return value
        except User.DoesNotExist:
            raise ValidationError(_("No user registered with this email"))


class ResetPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField(label=_("Token"), style={"show": False})
    password = PasswordField(
        label=_("New Password"), required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ["token", "password"]
        ref_name = None

    def validate_token(self, value):
        user = self.context.get("view").get_object()
        if not user.check_password_reset_token(value):
            raise ValidationError(_("Invalid token for this user"))
        return value
