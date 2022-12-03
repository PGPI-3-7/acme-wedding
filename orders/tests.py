from django.test import TestCase
from orders.models import Order, OrderItem
from base.tests import CatalogoTestCase

# Create your tests here.
class CensusReuseTestCase(CatalogoTestCase):
    def setUp(self):
        super().setUp()
    
    def test_census_reuse(self):
        self.login()

        data = {'first_name':'Iker','last_name':'Casillas','email':'casillas@gmail.com','address':'Santiago Bernabeu',
        'postal_code':'29660','city':'a'}
        self.orderItem = OrderItem.objects.create(order=self.order.id,product=self.product.id,price=10,amount=1)

        response = self.client.post('/orders/create',data=data)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        super().tearDown()
        