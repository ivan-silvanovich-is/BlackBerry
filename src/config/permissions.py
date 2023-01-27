from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperuserOrReadOnlyForStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_staff and request.method in SAFE_METHODS)


class IsSuperuserOrStaffWithoutPOST(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_staff and request.method != 'POST')


class IsCurrentUserOrOneStepHigherOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user and (
                obj == request.user or
                not obj.is_superuser and request.user.is_superuser or
                not obj.is_staff and not obj.is_superuser and request.user.is_staff
        )


class IsOwnerOrOneStepHigher(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (obj.user == request.user or
                                 not obj.user.is_superuser and request.user.is_superuser or
                                 not obj.user.is_staff and not obj.user.is_superuser and request.user.is_staff)


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and request.user.is_staff


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and obj.user == request.user


class IsOwnerOrIsStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user is None or request.user and (obj.user == request.user or request.user.is_staff)


class IsOwnerOrIsSuperuserOrReadOnlyForStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (
                    obj.user == request.user or request.user.is_superuser or request.user.is_staff and request.method in SAFE_METHODS)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user and obj.user == request.user
