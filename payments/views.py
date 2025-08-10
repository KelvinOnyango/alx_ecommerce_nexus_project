from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
import random
from orders.models import Order

class PaymentInitiateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Initiate payment with a provider (demo mode).",
        responses={
            200: "Payment initiated successfully.",
            400: "Invalid input data.",
            401: "Unauthorized."
        }
    )
    def post(self, request):
        # Simulate payment initiation
        demo_payment_id = f"demo_{random.randint(1000, 9999)}"
        return Response({"message": "Payment initiated successfully.", "payment_id": demo_payment_id}, status=status.HTTP_200_OK)

class PaymentWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Handle provider webhook (demo mode).",
        responses={
            200: "Webhook processed successfully.",
            400: "Invalid input data."
        }
    )
    def post(self, request):
        # Simulate webhook processing
        payment_status = random.choice(["Paid", "Failed"])
        order_id = request.data.get("order_id")

        try:
            order = Order.objects.get(id=order_id)
            order.payment_status = payment_status
            order.save()
            return Response({"message": "Webhook processed successfully.", "status": payment_status}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)