from rest_framework import serializers
from .models import Products

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Products
        fields = "__all__"