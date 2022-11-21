from rest_framework import serializers
from .models import Carts, Products, Reviews


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    class Meta:
        model = Reviews
        fields = "__all__"
    
    def create(self, validated_data):
        user = self.context.get('user')
        product = self.context.get('product')
        return product.reviews_set.create(user=user, **validated_data)



class ProductSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(read_only=True, many=True)
    avg_rating = serializers.CharField(read_only=True)
    rating_count = serializers.CharField(read_only=True)
    class Meta:
        model = Products
        fields = [
            "name",
            "description",
            "Brand",
            "price",
            "image",
            "category",
            "review",
            "avg_rating",
            "rating_count",
        ]


class CartSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    date = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Carts
        fields = ["product", "user", "date", "status"]

    def create(self, validated_data):
        user = self.context.get('user')
        product = self.context.get('product')
        return product.carts_set.create(**validated_data, user=user)