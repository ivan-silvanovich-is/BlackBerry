from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from config.permissions import IsOwner
from .models import *
from .serializers.user_serializers import *

__all__ = (
    'OrderViewSet',
    'DelivererViewSet',
    'PointViewSet',
)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user.id)
        else:
            return self.queryset


class DelivererViewSet(ReadOnlyModelViewSet):
    queryset = Deliverer.objects.all()
    serializer_class = DelivererSerializer
    lookup_field = 'slug'


class PointViewSet(ReadOnlyModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
