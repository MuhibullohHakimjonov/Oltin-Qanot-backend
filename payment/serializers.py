from rest_framework import serializers

from payment.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ['id', 'customer_name', 'address', 'total_cost', 'payment_method', 'is_paid']
