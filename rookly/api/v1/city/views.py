from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from rookly.api.v1.city.serializers import CitySerializer
from rookly.api.v1.metadata import Metadata
from rookly.common.models import City


class CityViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """
    Manager category.
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    metadata_class = Metadata
