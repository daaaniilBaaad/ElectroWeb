from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode, Product
from .serializers import NetworkNodeSerializer, NetworkNodeUpdateSerializer, ProductSerializer


class IsActiveEmployee(permissions.BasePermission):
    """Проверка прав доступа: только активные сотрудники."""
    def has_permission(self, request, view):
        return request.user and request.user.is_active


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """ViewSet для модели NetworkNode."""
    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["country"]
    search_fields = ["name", "city"]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return NetworkNodeUpdateSerializer
        return NetworkNodeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["network_node"]
