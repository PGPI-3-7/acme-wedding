from django.db import models
from base.models import Product
from django.urls import reverse
import random
import string
from enum import Enum

class TipoPago(Enum):
    T = "tarjeta"
    C = "contrarrembolso"

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    remember=models.BooleanField(default=False)
    remember_code=models.CharField(max_length=10,editable=False, blank=True,default='')
    id= models.CharField(max_length=10,editable=False, blank=True,default='', primary_key=True)
    braintree_id = models.CharField(max_length=150, blank=True)
    tipo_pago = models.CharField(max_length=100, choices=[(tag.value,tag.value) for tag in TipoPago])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())




    def save(self, *args, **kwargs):
        if self.remember==True and self.remember_code=='':
            self.remember_code=''.join([random.choice( string.ascii_uppercase +
                                            string.ascii_lowercase +
                                            string.digits)
                                            for n in range(10)])
        if self.id=='':
            self.id=''.join([random.choice( string.ascii_uppercase +
                                            string.ascii_lowercase +
                                            string.digits)
                                            for n in range(10)])
        super(Order, self).save(*args, **kwargs) # Call the "real" save() method.


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
    