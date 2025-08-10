from django.urls import path
from cart.views import CartView, CartItemAddView, CartItemUpdateView, CartItemDeleteView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('items/', CartItemAddView.as_view(), name='cart-item-add'),
    path('items/<int:id>/', CartItemUpdateView.as_view(), name='cart-item-update'),
    path('items/<int:id>/delete/', CartItemDeleteView.as_view(), name='cart-item-delete'),
]
