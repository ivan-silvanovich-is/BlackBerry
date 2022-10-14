from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and request.user.is_staff


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and obj.user == request.user


class IsOwnerOrIsStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user is None or request.user and (obj.user == request.user or request.user.is_staff)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user and obj.user == request.user
