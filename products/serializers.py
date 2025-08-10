from rest_framework import serializers
from .models import Product, Category, ProductReview
from django.contrib.auth import get_user_model
from django.db import models  # Import models for Avg

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        ref_name = "ProductsUserSerializer"  # Unique name for Swagger

class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        # pylint: disable=no-member
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    reviews = ProductReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 
            'category', 'category_id', 'image', 'is_active',
            'created_at', 'updated_at', 'reviews', 'average_rating'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0