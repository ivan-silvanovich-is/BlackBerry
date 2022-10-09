from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from config.permissions import IsOwner
from .serializers import *
from .models import *

__all__ = (
    'UserViewSet',
    'UserAddressViewSet',
)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class UserAddressViewSet(ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user.id)
        else:
            return self.queryset
