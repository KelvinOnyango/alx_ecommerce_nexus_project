from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from products.models import Product

class CartViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.cart = Cart.objects.create(user=self.user, is_active=True)
        self.product = Product.objects.create(name='Test Product', price=10.0)

    def test_get_cart(self):
        url = reverse('cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_item_to_cart(self):
        url = reverse('cart')
        data = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_cart_item(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        url = reverse('cart')
        data = {'product_id': self.product.id, 'quantity': 3}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_cart_item(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        url = reverse('cart')
        data = {'product_id': self.product.id}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
