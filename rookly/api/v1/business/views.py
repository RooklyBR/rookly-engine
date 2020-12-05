from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from rookly.api.v1.business.serializers import BusinessSerializer
from rookly.api.v1.metadata import Metadata
from rookly.common.models import Business


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
