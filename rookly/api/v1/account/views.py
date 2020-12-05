from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rookly.api.v1.metadata import Metadata
from rookly.authentication.models import User
from .serializers import LoginSerializer
from .serializers import RegisterUserSerializer


@method_decorator(
    name="create", decorator=swagger_auto_schema(responses={201: '{"token":"TOKEN"}'})
)
class LoginViewSet(mixins.CreateModelMixin, GenericViewSet):

    """
    Login Users
    """

    queryset = User.objects
    serializer_class = LoginSerializer
    lookup_field = ("username", "password")
    metadata_class = Metadata

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key},
            status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class RegisterUserViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    Register new user
    """

    queryset = User.objects
    serializer_class = RegisterUserSerializer
    lookup_field = ("email", "name", "cpf", "password", "telephone", "address_cep", "address_number", "address_complement", "birth_date")
    metadata_class = Metadata
