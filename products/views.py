from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg  # Added Avg import
from .models import Product, Category, ProductReview, ProductVariant
from cart.models import Cart
from .serializers import ProductSerializer, CategorySerializer, ProductReviewSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

class CategoryListCreateView(generics.ListCreateAPIView):
    # pylint: disable=no-member
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @swagger_auto_schema(operation_description="List and create categories.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new category.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # pylint: disable=no-member
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductListCreateView(generics.ListCreateAPIView):
    # pylint: disable=no-member
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']

    @swagger_auto_schema(operation_description="List and create products with filters.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new product.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        # pylint: disable=no-member
        queryset = Product.objects.select_related('category').prefetch_related('reviews')
        
        # Filter by minimum price if provided
        min_price = self.request.query_params.get('min_price')
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
            
        # Filter by maximum price if provided
        max_price = self.request.query_params.get('max_price')
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
            
        return queryset

class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    # pylint: disable=no-member
    queryset = Product.objects.select_related('category').prefetch_related('reviews')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductReviewCreateView(generics.CreateAPIView):
    # pylint: disable=no-member
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Retrieve product statistics.")
    def get(self, request):
        _ = request  # Mark request as used
        stats = {
            # pylint: disable=no-member
            'total_products': Product.objects.count(),
            'active_products': Product.objects.filter(is_active=True).count(),
            'average_price': Product.objects.aggregate(Avg('price'))['price__avg'],
            'categories_count': Category.objects.count()
        }
        return Response(stats)

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the active cart.",
        responses={
            200: "Cart retrieved successfully.",
            404: "Cart not found."
        }
    )
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        return Response({"id": cart.id, "message": "Cart retrieved successfully."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Add an item to the cart.",
        request_body=ProductSerializer,
        responses={
            201: "Item added to cart successfully.",
            400: "Invalid input data."
        }
    )
    def post(self, request):
        # Logic to add an item to the cart
        return Response({"message": "Item added to cart successfully."}, status=status.HTTP_201_CREATED)

class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Initiate checkout.",
        responses={
            200: "Checkout initiated successfully.",
            400: "Invalid input data."
        }
    )
    def post(self, request):
        # Validate the cart
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        if not cart or not cart.items.exists():
            return Response({"error": "Cart is empty or not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order (simplified logic)
        order = {
            "user": request.user.id,
            "items": list(cart.items.values("product_id", "quantity")),
            "total": sum(item.product.price * item.quantity for item in cart.items.all())
        }

        # Clear the cart
        cart.items.all().delete()
        cart.is_active = True
        cart.save()

        # Send confirmation (placeholder logic)
        confirmation_message = f"Order created successfully for user {request.user.id}."

        return Response({"message": "Checkout initiated successfully.", "order": order, "confirmation": confirmation_message}, status=status.HTTP_200_OK)

class ProductVariantListCreateView(generics.ListCreateAPIView):
    # pylint: disable=no-member
    queryset = ProductVariant.objects.select_related('product')
    serializer_class = ProductSerializer  # Replace with a dedicated ProductVariantSerializer if available
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'price']
    search_fields = ['name']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']

    @swagger_auto_schema(operation_description="List and create product variants.")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new product variant.")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
