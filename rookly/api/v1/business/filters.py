from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters

from rookly.common.models import BusinessService, Business


class BusinessServiceFilter(filters.FilterSet):
    class Meta:
        model = BusinessService
        fields = ["type_user", "subcategory"]

    type_user = filters.ChoiceFilter(
        field_name="business__type_user",
        help_text=_("type user"),
        choices=Business.TYPE_USER_CHOICES,
    )

    subcategory = filters.CharFilter(
        field_name="business_category__subcategory__id", help_text=_("subcategory")
    )
