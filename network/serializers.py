from rest_framework import serializers
from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "model", "release_date", "network_node"]


class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            "id", "name", "email", "country", "city", "street", "house_number",
            "supplier", "supplier_name", "debt_to_supplier", "created_at", "level", "products"
        ]
        read_only_fields = ["debt_to_supplier", "created_at", "level"]


class NetworkNodeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = [
            "name", "email", "country", "city", "street", "house_number",
            "supplier"
        ]
