from django.test import TestCase
from .models import Category, Product

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from time import sleep


class CatalogoTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.category=Category.objects.create(name="category test")
        self.product=Product.objects.create(category=self.category,
                                name="test",
                                image="agotado.png",
                                description="test description",
                                price=10.00,
                                amount=10)
        
    
    def tearDown(self):
        super().tearDown()
        self.product=None
        self.category=None

    def test_product_category_exist(self):
        product = Product.objects.get(name="test")
        category=product.category
        self.assertEqual(product.name, 'test')
        self.assertEqual(product.image, 'agotado.png')
        self.assertEqual(product.description, 'test description')
        self.assertEqual(product.price, 10.00)
        self.assertEqual(product.amount, 10)
        self.assertEqual(category.name, 'category test')
    
    def test_product_unavailable(self):
        product = Product.objects.get(name="test")
        self.assertTrue(product.available)
        product.amount=0
        product.save()
        self.assertFalse(product.available)

    def test_enter_inicio(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_enter_catalogo(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

class SeleniumInicioTestCase(StaticLiveServerTestCase):
    
    def setUp(self):
        #Load base test functionality for decide
        super().setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)           
            
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()
        self.product=None
        self.category=None

    def test_enter_inicio(self):

        self.category=Category.objects.create(name="category test")
        self.product=Product.objects.create(category=self.category,
                                name="test",
                                image="agotado.png",
                                description="test description",
                                price=10.00,
                                amount=10)
       
        Product.objects.create(category=self.category,
                                name="test2",
                                image="agotado2.png",
                                description="test description 2",
                                price=11.00,
                                amount=9)
        
        Product.objects.create(category=self.category,
                                name="test3",
                                image="agotado3.png",
                                description="test description 3",
                                price=12.00,
                                amount=11)
        
        self.driver.get(f'{self.live_server_url}')
        self.assertTrue(len(self.driver.find_elements(By.ID, "carouselExampleCaptions"))==1)
        self.assertTrue(len(self.driver.find_elements(By.CLASS_NAME, "carousel-item"))==3)

    def test_enter_inicio_negative(self):
        self.product=None
        self.category=None
        self.driver.get(f'{self.live_server_url}')
        self.assertTrue(len(self.driver.find_elements(By.CLASS_NAME, "btn-danger"))==1)







    




       

