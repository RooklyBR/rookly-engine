from rest_framework import permissions

from rookly.api.v1 import READ_METHODS, WRITE_METHODS, ADMIN_METHODS


class BusinessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in READ_METHODS:
                return True
            if request.method in WRITE_METHODS or request.method in ADMIN_METHODS:
                return obj.user == request.user
        return False


class BusinessServicePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in READ_METHODS:
                return True
            if request.method in WRITE_METHODS or request.method in ADMIN_METHODS:
                return obj.business.user == request.user
        return False
