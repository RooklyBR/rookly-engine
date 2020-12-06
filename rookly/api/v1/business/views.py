from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from rookly.api.v1.business.filters import BusinessServiceFilter
from rookly.api.v1.business.serializers import (
    BusinessSerializer,
    BusinessServiceSerializer,
)
from rookly.api.v1.metadata import Metadata
from rookly.common.models import Business, BusinessService


class BusinessViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Manager business.
    """

    queryset = Business.objects
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
    metadata_class = Metadata


class BusinessServiceViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Manager business.
    """

    queryset = BusinessService.objects
    serializer_class = BusinessServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_class = BusinessServiceFilter
    # filter_backends = [DjangoFilterBackend, SearchFilter]
    # search_fields = ["$business_category__subcategory__name", "^business_category__subcategory__name", "=business_category__subcategory__name"]
    metadata_class = Metadata
