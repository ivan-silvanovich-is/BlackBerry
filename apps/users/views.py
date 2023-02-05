from django.db.models import Q
from djoser import utils
from djoser.conf import settings
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.core.permissions import IsOwnerOrOneStepHigher
from .filters.staff_filters import *
from .models import *
from .serializers.admin_serializers import *
from .serializers.staff_serializers import *
from .serializers.user_serializers import *

__all__ = (
    'UserViewSet',
    'AddressViewSet',
)


class UserViewSet(DjoserUserViewSet):
    staff_filterset_class = StaffUserFilter

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = settings.PERMISSIONS.me

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create" and self.request.user.is_superuser:
            return AdminUserSerializer
        elif self.action == "create" and self.request.user.is_staff:
            return StaffUserSerializer

        serializer_class = super().get_serializer_class()
        if serializer_class != self.serializer_class:
            return serializer_class

        if self.request.user.is_superuser:
            return AdminUserSerializer
        elif self.request.user.is_staff:
            return StaffUserSerializer
        elif self.action == 'retrieve' and self.request.user == self.get_object():
            return PrivateUserSerializer
        else:
            return serializer_class

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()

        if not request.user.is_superuser or user.is_superuser:
            serializer = self.get_serializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)

        if user == request.user:
            utils.logout_user(self.request)

        self.perform_destroy(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    permission_classes = (IsOwnerOrOneStepHigher, IsAuthenticated,)
    staff_filterset_class = StaffAddressFilter

    def get_queryset(self):
        user = self.request.user
        if self.action != 'list':
            return self.queryset
        elif user.is_superuser:
            return self.queryset.filter(Q(user=user) | Q(user__is_superuser=False))
        elif user.is_staff:
            return self.queryset.filter(Q(user=user) | Q(user__is_staff=False) & Q(user__is_superuser=False))
        else:
            return self.queryset.filter(user=user)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffAddressSerializer
        else:
            return AddressSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
