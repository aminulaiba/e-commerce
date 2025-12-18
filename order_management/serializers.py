from rest_framework import serializers
from cart.views import Order, OrderItem







class OrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", default=None)
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product_img_url = serializers.URLField(source="product.image", default=None)
    class Meta:
        model = OrderItem
        fields = '__all__'