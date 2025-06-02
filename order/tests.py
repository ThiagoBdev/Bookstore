from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from order.models import Order
from product.models import Product
from order.serializers import OrderSerializer

class OrderSerializerTest(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='cliente1', password='senha123')
        
        
        self.produto1 = Product.objects.create(title='Produto 1', price=50)
        self.produto2 = Product.objects.create(title='Produto 2', price=30)
        
        
        self.pedido = Order.objects.create(user=self.user)
        self.pedido.product.set([self.produto1, self.produto2])

    def test_order_serializer_data(self):
        
        serializer = OrderSerializer(self.pedido)
        data = serializer.data
        
        
        self.assertEqual(len(data['product']), 2)
        self.assertEqual(data['product'][0]['id'], self.produto1.id)
        self.assertEqual(data['product'][1]['id'], self.produto2.id)
        
        
        self.assertEqual(data['total'], 80)
        
        
        self.assertEqual(data['user'], self.user.id)

    def test_order_serializer_create(self):
        
        data = {
            'user': self.user.id,
            'products_id': [self.produto1.id, self.produto2.id]
        }
        
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        
        order = serializer.save(user=self.user)
        
        
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product.count(), 2)
        self.assertIn(self.produto1, order.product.all())
        self.assertIn(self.produto2, order.product.all())
