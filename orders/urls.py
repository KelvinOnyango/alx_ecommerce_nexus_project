from django.urls import path
from orders.views import OrderListView, OrderDetailView, OrderCancelView, ShipmentCreateView, ReturnRequestCreateView, OrderCreateView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:order_id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('<int:order_id>/ship/', ShipmentCreateView.as_view(), name='shipment-create'),
    path('<int:order_id>/returns/', ReturnRequestCreateView.as_view(), name='return-request-create'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
]