from django.http import HttpRequest
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from cart.cart import Cart
from base import models as base_models
from acme_wedding.test_utils import create_product
import datetime
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

IMAGE_PATH = 'media/agotado.png'

class CartTest(TestCase):
    def setUp(self):
        session = SessionStore(None)
        session.clear()
        session.cycle_key()
        session[settings.CART_SESSION_ID] = {}
        session.save()
        self.session = session

        self.test_category, self.test_product = create_product()

        return super().setUp()

    def tearDown(self):
        self.cart.clear()
        return super().tearDown()

    def test_create_cart(self):
        request = HttpRequest()
        request.session = self.session
        self.cart = Cart(request)

        self.assertEqual(self.cart.cart,{})

    def test_add(self):
        self.test_create_cart()

        self.cart.add(self.test_product)
        self.assertEqual(len(self.cart),1)

    def test_remove(self):
        self.test_create_cart()
        self.test_add()
        self.assertEqual(len(self.cart),1)

        self.cart.remove(self.test_product)
        self.assertEqual(len(self.cart),0)

    def test_add_multiple(self):
        self.test_create_cart()

        products = []
        for i in range(3):
            test_product = base_models.Product()
            test_product.amount = 10
            test_product.available = True
            test_product.name = 'Producto Test {}'.format(i)
            test_product.slug = 'producto-test-{}'.format(i)
            test_product.description = 'Producto de prueba para la aplicacion'
            test_product.image = 'TestImage{}'.format(i)
            test_product.price = 100
            test_product.created = datetime.datetime.now()
            test_product.updated = datetime.datetime.now()
            test_product.category = self.test_category
            test_product.save()
            products.append(test_product)
        
        for p in products:
            self.cart.add(p,override_quantity=True)

        total_sum = sum(p['quantity']*p['price'] for p in self.cart)
        self.assertEqual(total_sum,self.cart.get_total_price())

class CartViewTest(StaticLiveServerTestCase):

    def setUp(self):
        super().setUp()

        self.test_category, self.test_product = create_product()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        super().tearDown()
        self.driver.quit()

    def test_cart_detail(self):
        self.driver.get('{}/cart'.format(self.live_server_url))
        self.driver.find_element(By.CSS_SELECTOR,'a.btn.btn-outline-secondary.mx-auto').click()
        self.assertTrue(self.driver.current_url=='{}/catalogo'.format(self.live_server_url))

    def test_cart_add(self):
        self.driver.get('{}/catalogo'.format(self.live_server_url))
        self.driver.find_element(By.CSS_SELECTOR,'button.btn.btn-primary').click()
        self.assertTrue(len(self.driver.find_elements(By.ID,'item-{}'.format(self.test_product.pk)))==1)
