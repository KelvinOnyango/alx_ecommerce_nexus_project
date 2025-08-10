from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, ShipmentSerializer, ReturnRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from cart.models import Cart
from products.models import Product
import logging

logger = logging.getLogger(__name__)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List user orders (sellers see sales).",
        responses={
            200: OrderSerializer(many=True),
            401: "Unauthorized."
        }
    )
    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(queryset, many=True).data)

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve order details.",
        responses={
            200: OrderSerializer,
            404: "Order not found.",
            401: "Unauthorized."
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class OrderCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Cancel an order if eligible.",
        responses={
            200: "Order canceled successfully.",
            400: "Invalid input data.",
            401: "Unauthorized."
        }
    )
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            if order.status == "Canceled":
                return Response({"error": "Order is already canceled."}, status=status.HTTP_400_BAD_REQUEST)

            order.status = "Canceled"
            order.save()

            return Response({"message": "Order canceled successfully."}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

class ShipmentCreateView(generics.CreateAPIView):
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a shipment (seller/admin).",
        request_body=ShipmentSerializer,
        responses={
            201: "Shipment created successfully.",
            400: "Invalid input data.",
            401: "Unauthorized."
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ReturnRequestCreateView(generics.CreateAPIView):
    serializer_class = ReturnRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a return request.",
        request_body=ReturnRequestSerializer,
        responses={
            201: "Return request created successfully.",
            400: "Invalid input data.",
            401: "Unauthorized."
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create an order from the cart.",
        responses={
            201: "Order created successfully.",
            400: "Invalid input data.",
            401: "Unauthorized."
        }
    )
    def post(self, request):
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart:
            cart = Cart.objects.create(user=request.user, is_active=True)
        if not cart.items.exists():
            return Response({"error": "Cart is empty or not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_amount=sum(item.product.price * item.quantity for item in cart.items.all()),
            status="Pending",
            payment_status="Unpaid"
        )

        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear the cart
        cart.items.all().delete()
        cart.is_active = False
        cart.save()

        return Response({"message": "Order created successfully.", "order_id": order.id}, status=status.HTTP_201_CREATED)

class CartAddItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add an item to the cart.",
        responses={
            200: "Item added successfully.",
            400: "Invalid input data.",
            401: "Unauthorized."
        }
    )
    def post(self, request):
        # Check if the user has an active cart
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)

        # Extract item details from the request
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Add or update the item in the cart
        cart_item, item_created = cart.items.get_or_create(product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()

        # Log the value of is_active before updating
        logger.debug(f"Cart is_active before updating: {cart.is_active}")

        # Ensure the cart is active using update()
        Cart.objects.filter(id=cart.id).update(is_active=True)
        logger.debug(f"Cart is_active after updating: {Cart.objects.get(id=cart.id).is_active}")

        # Refresh the cart object from the database
        cart.is_active = True
        cart.save()
        logger.debug(f"Cart is_active after refreshing: {cart.is_active}")

        # Log the value of is_active after refreshing
        print(f"Cart is_active after refreshing: {cart.is_active}")

        return Response({"message": "Item added successfully."}, status=status.HTTP_200_OK)

class CartDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete the user's cart.",
        responses={
            200: "Cart deleted successfully.",
            404: "Cart not found.",
            401: "Unauthorized."
        }
    )
    def delete(self, request):
        try:
            cart = Cart.objects.get(user=request.user, is_active=True)
            cart.delete()
            return Response({"message": "Cart deleted successfully."}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the user's cart details.",
        responses={
            200: "Cart details retrieved successfully.",
            404: "Cart not found.",
            401: "Unauthorized."
        }
    )
    def get(self, request):
        try:
            # Ensure only one active cart exists for the user
            carts = Cart.objects.filter(user=request.user, is_active=True)
            if carts.count() > 1:
                return Response({"error": "Multiple active carts found. Please contact support."}, status=status.HTTP_400_BAD_REQUEST)

            cart = carts.first()
            if not cart:
                return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

            cart_items = cart.items.all()
            return Response({
                "cart": {
                    "id": cart.id,
                    "items": [
                        {
                            "product": item.product.name,
                            "quantity": item.quantity,
                            "price": item.product.price
                        } for item in cart_items
                    ]
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving cart: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)