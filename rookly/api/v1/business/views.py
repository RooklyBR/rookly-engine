from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from rookly.api.v1.business.filters import BusinessServiceFilter
from rookly.api.v1.business.serializers import (
    BusinessSerializer,
    BusinessServiceSerializer,
)
from rookly.api.v1.business.validators import (
    BusinessServicePermission,
    BusinessPermission,
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
    permission_classes = [IsAuthenticated, BusinessPermission]
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
    permission_classes = [IsAuthenticatedOrReadOnly, BusinessServicePermission]
    filter_class = BusinessServiceFilter
    metadata_class = Metadata


class MyBusinessServiceViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    Manager business.
    """

    queryset = BusinessService.objects
    serializer_class = BusinessServiceSerializer
    permission_classes = [IsAuthenticated]
    metadata_class = Metadata

    def get_queryset(self):
        return self.queryset.filter(business__user=self.request.user)
