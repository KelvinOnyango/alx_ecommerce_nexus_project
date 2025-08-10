from django.test import TestCase
from cart.models import Cart, CartItem
from django.contrib.auth import get_user_model
from products.models import Product

class CartModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.cart = Cart.objects.create(user=self.user, is_active=True)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user, self.user)
        self.assertTrue(self.cart.is_active)

class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.cart = Cart.objects.create(user=self.user, is_active=True)
        self.product = Product.objects.create(name='Test Product', price=10.0)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)
