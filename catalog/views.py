from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer
from drf_yasg.utils import swagger_auto_schema

class CategoryTreeView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve category tree listing (with child categories).",
        responses={
            200: CategorySerializer(many=True),
            400: "Invalid input data."
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve brand listing.",
        responses={
            200: BrandSerializer(many=True),
            400: "Invalid input data."
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve product listing with filters and pagination.",
        responses={
            200: ProductSerializer(many=True),
            400: "Invalid input data."
        }
    )
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.filter(
            category=request.query_params.get('category'),
            brand=request.query_params.get('brand'),
            price__gte=request.query_params.get('min_price'),
            price__lte=request.query_params.get('max_price'),
            is_active=request.query_params.get('is_active')
        ).order_by(request.query_params.get('ordering'))
        return Response(ProductSerializer(queryset, many=True).data)