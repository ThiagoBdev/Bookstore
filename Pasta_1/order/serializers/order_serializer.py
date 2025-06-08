from rest_framework import serializers

from order.models import Order
from product.models import Product
from product.serializers.category_serializer import CategorySerializer
from product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)
    products_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, many=True
    )
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total

    class Meta:
        model = Order
        fields = ["product", "total", "user", "products_id"]
        extra_kwargs = {"product": {"required": False}}

    def create(self, validated_data):
        products = validated_data.pop('products_id')
        order = Order.objects.create(user=validated_data['user'])
        order.product.set(products)
        return order
