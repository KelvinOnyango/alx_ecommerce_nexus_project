from django.test import TestCase
from cart.serializers import CartSerializer, CartItemSerializer
from cart.models import Cart, CartItem
from django.contrib.auth import get_user_model
from products.models import Product

class CartSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.cart = Cart.objects.create(user=self.user, is_active=True)
        self.serializer = CartSerializer(instance=self.cart)

    def test_cart_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['user'], self.user.id)
        self.assertTrue(data['is_active'])

class CartItemSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.cart = Cart.objects.create(user=self.user, is_active=True)
        self.product = Product.objects.create(name='Test Product', price=10.0)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.serializer = CartItemSerializer(instance=self.cart_item)

    def test_cart_item_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['cart'], self.cart.id)
        self.assertEqual(data['product'], self.product.id)
        self.assertEqual(data['quantity'], 2)
