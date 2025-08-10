from django.urls import path
from .views import (
    ProductListCreateView,
    ProductRetrieveUpdateDeleteView,
    CategoryListCreateView,
    CategoryRetrieveUpdateDeleteView,
    ProductReviewCreateView,
    ProductStatsView,
    CartView,
    CheckoutView
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='product-retrieve-update-delete'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDeleteView.as_view(), name='category-retrieve-update-delete'),
    path('products/<int:product_pk>/reviews/', ProductReviewCreateView.as_view(), name='product-review-create'),
    path('stats/', ProductStatsView.as_view(), name='product-stats'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]