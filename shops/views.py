from rest_framework import generics, permissions
from shops.models import Shop
from shops.serializers import ShopSerializer
from drf_yasg.utils import swagger_auto_schema

class ShopListView(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="List all shops (searchable).",
        responses={
            200: ShopSerializer(many=True),
            400: "Invalid input data."
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ShopCreateView(generics.CreateAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new shop (seller only).",
        request_body=ShopSerializer,
        responses={
            201: "Shop successfully created.",
            400: "Invalid input data.",
            403: "Permission denied."
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ShopDetailView(generics.RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve shop details.",
        responses={
            200: ShopSerializer,
            404: "Shop not found."
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)