from rest_framework import serializers
from ..models import Property


class PropertySerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Property
        fields = ['id', 'address', 'price', 'status', 'sale_type', 'created_at', 'modified_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'modified_at', 'created_by']

    def get_created_at(self, obj):
        return int(obj.created_at.timestamp())

    def get_modified_at(self, obj):
        return int(obj.modified_at.timestamp())

