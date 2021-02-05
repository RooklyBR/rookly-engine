import re
from django.utils.translation import ugettext_lazy as _
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from rookly.api.v1 import READ_METHODS, WRITE_METHODS


class CPFCNPJValidator(object):
    def __call__(self, value):
        reg = re.compile(
            r"([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})"
        )
        if not reg.match(value):
            raise ValidationError(_("Enter a valid CPF or CNPJ."))


class BusinessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in READ_METHODS:
                return True
            if request.method in WRITE_METHODS:
                return obj.user == request.user
            return True
        return False


class BusinessServicePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in READ_METHODS:
                return True
            if request.method in WRITE_METHODS:
                return obj.business.user == request.user
            return True
        return False
