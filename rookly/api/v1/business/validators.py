import re

from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError, PermissionDenied


class CPFCNPJValidator(object):
    def __call__(self, value):
        reg = re.compile(
            r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})"
        )
        if not reg.match(value):
            raise ValidationError(_("Enter a valid CPF or CNPJ."))


class CanContributeBusinessValidator(object):
    def __call__(self, value):
        if self.request.user.is_authenticated:
            if not self.request.user == value.user:
                raise PermissionDenied(_("You can't contribute in this business"))

    def set_context(self, serializer):
        self.request = serializer.context.get("request")


class ServiceExistsCategoryValidator(object):
    def __call__(self, attrs):
        business = attrs.get("business")
        business_category = attrs.get("business_category")

        if not business and not business_category:
            raise ValidationError(_("Specify the business UUID and category ID"))

        if business.business_category.filter(
            subcategory=business_category.get("subcategory").pk
        ).exists():
            raise ValidationError(
                _("You already have a registered service with this category")
            )
