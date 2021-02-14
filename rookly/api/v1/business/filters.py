from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters

from rookly.common.models import BusinessService, Business


class BusinessServiceFilter(filters.FilterSet):
    class Meta:
        model = BusinessService
        fields = [
            "type_user",
            "payment_type",
            "subcategory",
            "category",
            "city",
            "state",
            "user",
            "price",
        ]

    type_user = filters.ChoiceFilter(
        field_name="business__type_user",
        help_text=_("type user"),
        choices=Business.TYPE_USER_CHOICES,
    )

    payment_type = filters.ChoiceFilter(
        field_name="payment_type",
        help_text=_("type payment"),
        choices=BusinessService.TYPE_PAYMENT_CHOICES,
    )

    subcategory = filters.CharFilter(
        field_name="business_category__subcategory__id", help_text=_("subcategory")
    )

    category = filters.CharFilter(
        field_name="business_category__subcategory__category__id",
        help_text=_("category"),
    )

    city = filters.CharFilter(
        field_name="business__city__id", method="filter_city", help_text=_("city")
    )

    state = filters.CharFilter(
        field_name="business__city__state__id",
        method="filter_state",
        help_text=_("state"),
    )

    user = filters.CharFilter(
        field_name="business__user", method="filter_user", help_text=_("user")
    )

    price = filters.RangeFilter(field_name="price", method="filter_price")

    def filter_city(self, queryset, name, value):
        return queryset.filter(business__city__pk=value)

    def filter_state(self, queryset, name, value):
        return queryset.filter(business__city__state__pk=value)

    def filter_user(self, queryset, name, value):
        return queryset.filter(business__user__pk=value)

    def filter_price(self, queryset, name, value):
        value_min = float(0.0 if value.start is None else value.start)

        if value.stop is None:
            query = queryset.filter(
                Q(price__gte=value_min),
            )
        else:
            query = queryset.filter(
                Q(price__gte=value_min),
                Q(price__lte=float(value.stop)),
            )
        return query
