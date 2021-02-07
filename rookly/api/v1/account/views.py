import filetype
from django.db.models import Exists, OuterRef
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status, mixins, permissions, parsers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import UnsupportedMediaType
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rookly.api.v1.metadata import Metadata
from rookly.authentication.models import User
from rookly.common.models import Business
from .serializers import LoginSerializer, UserSerializer, UserPhotoSerializer
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
    lookup_field = (
        "email",
        "name",
        "cpf",
        "password",
        "telephone",
        "address_cep",
        "address_number",
        "address_complement",
        "birth_date",
    )
    metadata_class = Metadata


class MyUserProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Manager current user profile.
    retrieve:
    Get current user profile
    update:
    Update current user profile.
    partial_update:
    Update, partially, current user profile.
    """

    serializer_class = UserSerializer
    queryset = User.objects
    lookup_field = None
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        request = self.request
        user = request.user

        # May raise a permission denied
        self.check_object_permissions(self.request, user)

        return user

    @action(
        detail=True,
        methods=["POST"],
        url_name="profile-upload-photo",
        parser_classes=[parsers.MultiPartParser],
        serializer_class=UserPhotoSerializer,
    )
    def upload_photo(self, request, **kwargs):  # pragma: no cover
        f = request.FILES.get("file")

        serializer = UserPhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if filetype.is_image(f):
            self.request.user.photo = f
            self.request.user.save(update_fields=["photo"])

            return Response({"photo": self.request.user.photo.url})
        try:
            raise UnsupportedMediaType(
                filetype.get_type(f.content_type).extension,
                detail=_("We accept images only in the formats: .png, .jpeg, .gif"),
            )
        except Exception:
            raise UnsupportedMediaType(
                None,
                detail=_("We accept images only in the formats: .png, .jpeg, .gif"),
            )


class UserProfileViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """
    Get user profile
    """

    serializer_class = UserSerializer
    queryset = User.objects
    lookup_field = "pk"

    def get_queryset(self):
        queryset = User.objects.annotate(
            have_business=Exists(Business.objects.filter(user=OuterRef("id")))
        )
        return queryset.filter(have_business=True)
