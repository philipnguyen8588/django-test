import django_filters
from django_filters import FilterSet
from rest_framework import (
    mixins,
    permissions,
    viewsets, )

from .permissions import IsOwnerOrSuperuser
from .serializers import PropertySerializer
from ..models import Property, Status


class PropertyFilter(FilterSet):
    address = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.CharFilter(lookup_expr='exact')
    sale_type = django_filters.CharFilter(lookup_expr='exact')
    price = django_filters.NumberFilter(field_name='price', lookup_expr='exact')
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Property
        fields = ['address', 'status', 'sale_type', 'price', 'price_gte', 'price_lte']


class PropertyViewSet(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]
    filterset_class = PropertyFilter

    ordering_fields = ['price', 'created_at', 'modified_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Properties marked as "deleted" should not be returned
        # unless the filter specifically asks for deleted properties
        if not self.request.query_params.get('include_deleted', '').lower() == 'true':
            queryset = queryset.exclude(status=Status.DELETED)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # AllowAny for list and retrieve
            return [permissions.AllowAny()]
        else:
            # restrict for others
            return super().get_permissions()
