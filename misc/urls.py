from django.urls import path
from .views import ProductMetricsView, UnifiedSearchView

urlpatterns = [
    path('stats/products/', ProductMetricsView.as_view(), name='product-metrics'),
    path('search/', UnifiedSearchView.as_view(), name='unified-search'),
]