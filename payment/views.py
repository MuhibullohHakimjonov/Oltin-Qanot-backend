from click_up.views import ClickWebhook
from rest_framework.response import Response
from click_up import ClickUp
from config import settings
from rest_framework.views import APIView
from .serializers import OrderCreateSerializer
from click_up.models import ClickTransaction
from .models import Order

click_up = ClickUp(service_id=settings.CLICK_SETTINGS['service_id'],
				   merchant_id=settings.CLICK_SETTINGS['merchant_id'])


class ClickWebhookAPIView(ClickWebhook):
	def successfully_payment(self, params):
		"""
		successfully payment method process you can ovveride it
		"""
		transaction = ClickTransaction.objects.get(
			transaction_id=params.click_trans_id
		)
		order = Order.objects.get(id=transaction.account_id)
		order.is_paid = True
		order.save()
		print(f"payment successful params: {params}")

	def cancelled_payment(self, params):
		"""
		cancelled payment method process you can ovveride it
		"""
		transaction = ClickTransaction.objects.get(
			transaction_id=params.click_trans_id
		)
		if transaction.state == ClickTransaction.CANCELLED:
			order = Order.objects.get(id=transaction.account_id)
			order.is_paid = False
			order.save()
		print(f"payment cancelled params: {params}")


class OrderCreateView(APIView):
	serializers_class = OrderCreateSerializer

	def post(self, request):
		serializer = self.serializers_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		result = {
			"order": serializer.data
		}

		if serializer.data['payment_method'] == 'click':
			paylink = click_up.initializer.generate_pay_link(
				id=serializer.data['id'],
				amount=serializer.data['total_cost'],
				return_url="https://ezgu.uz/"
			)
			result['payment_link'] = paylink
		return Response(result)
