from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from rookly.api.v1.category.serializers import CategorySerializer
from rookly.api.v1.metadata import Metadata
from rookly.common.models import Category


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """
    Manager category.
    """

    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    metadata_class = Metadata
