from rest_framework import serializers
from orders.models import Order, Shipment, ReturnRequest

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'tax', 'shipping_amount', 'status', 'payment_status']

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['id', 'order', 'tracking_number', 'carrier', 'status', 'shipped_at', 'delivered_at']

class ReturnRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRequest
        fields = ['id', 'order', 'reason', 'status', 'created_at']
