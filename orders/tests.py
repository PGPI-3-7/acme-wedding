from django.test import TestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


from cart.cart import Cart
from base import models as base_models
import datetime
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from django.http import HttpRequest


from time import sleep


def create_product():
    test_category = base_models.Category()
    test_category.name = 'Test Category'
    test_category.slug = 'test-category'
    test_category.save()

    test_product = base_models.Product()
    test_product.amount = 10
    test_product.available = True
    test_product.name = 'Producto Test'
    test_product.slug = 'producto-test'
    test_product.description = 'Producto de prueba para la aplicacion'
    test_product.image = 'ImagenDePruebaXiquillo'
    test_product.price = 100
    test_product.created = datetime.datetime.now()
    test_product.updated = datetime.datetime.now()
    test_product.category = test_category
    test_product.save()
    return [test_category,test_product]


class SeleniumInicioTestCase(StaticLiveServerTestCase):
    
    def setUp(self):
        #Load base test functionality for decide
        super().setUp()

        options = webdriver.ChromeOptions()
        options.headless = True


        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920,1080)

        session = SessionStore(None)
        session.clear()
        session.cycle_key()
        session[settings.CART_SESSION_ID] = {}
        session.save()
        self.session = session

        self.test_category, self.test_product = create_product() 
        request = HttpRequest()
        request.session = self.session
        self.cart = Cart(request)     
        self.cart.add(self.test_product)  
            
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()
        self.cart.clear()

    def test_contrareembolso_positive(self):
        self.driver.get(f'{self.live_server_url}/catalogo')
        self.driver.find_element(By.CSS_SELECTOR, ".col-lg-12 > .btn").click()
        self.assertTrue(len(self.driver.find_elements_by_xpath("//*[contains(text(), 'Comprar')]"))==1)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Comprar')]").click()
        self.driver.find_element(By.ID, "id_first_name").send_keys("Test")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Test2")
        self.driver.find_element(By.ID, "id_email").send_keys("correotest@gmail.com")
        self.driver.find_element(By.ID, "id_address").send_keys("test, 23, 8")
        self.driver.find_element(By.ID, "id_postal_code").send_keys("41008")
        self.driver.find_element(By.ID, "id_city").send_keys("Test")
        dropdown = Select(self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(8) > #id_tipo_pago"))
        dropdown.select_by_visible_text('contrarrembolso')
        self.driver.find_element_by_xpath("//input[@name='accept_terms']").click()
        self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(10) > .btn").click()
        self.assertTrue(len(self.driver.find_elements(By.ID, "gracias"))==1)

    def test_tarjeta_positive(self):
        self.driver.get(f'{self.live_server_url}/catalogo')
        self.driver.find_element(By.CSS_SELECTOR, ".col-lg-12 > .btn").click()
        self.assertTrue(len(self.driver.find_elements_by_xpath("//*[contains(text(), 'Comprar')]"))==1)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Comprar')]").click()
        self.driver.find_element(By.ID, "id_first_name").click()
        self.driver.find_element(By.ID, "id_first_name").send_keys("Test")
        self.driver.find_element(By.ID, "id_last_name").click()
        self.driver.find_element(By.ID, "id_last_name").send_keys("Test2")
        self.driver.find_element(By.ID, "id_email").click()
        self.driver.find_element(By.ID, "id_email").send_keys("correotest@gmail.com")
        self.driver.find_element(By.ID, "id_address").click()
        self.driver.find_element(By.ID, "id_address").send_keys("test, 23, 8")
        self.driver.find_element(By.ID, "id_postal_code").click()
        self.driver.find_element(By.ID, "id_postal_code").send_keys("41008")
        self.driver.find_element(By.ID, "id_city").click()
        self.driver.find_element(By.ID, "id_city").send_keys("Test")
        self.driver.find_element(By.ID, "id_remember").click()
        dropdown = Select(self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(8) > #id_tipo_pago"))
        dropdown.select_by_visible_text('tarjeta')
        self.driver.find_element(By.ID, "id_accept_terms").click()
        self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(10) > .btn").click()
        sleep(3)#Necesario para cargar braintree
        self.assertTrue(len(self.driver.find_elements(By.ID, "processTitle"))==1)
        self.driver.switch_to.frame(0)
        self.driver.find_element(By.ID, "credit-card-number").click()
        self.driver.find_element(By.ID, "credit-card-number").send_keys("4111 1111 1111 1111")
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(1)
        self.driver.find_element(By.ID, "cvv").click()
        self.driver.find_element(By.ID, "cvv").send_keys("123")
        self.driver.switch_to.default_content()
        self.driver.find_element(By.ID, "expiration-date").click()
        self.driver.switch_to.frame(2)
        self.driver.find_element(By.ID, "expiration").click()
        self.driver.find_element(By.ID, "expiration").send_keys("12 / 34")
        self.driver.switch_to.default_content()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-lg").click()
        sleep(2)#Necesario para enviar braintree
        self.assertTrue(len(self.driver.find_elements(By.ID, "gracias"))==1)


    def test_enter_inicio_negative(self):
        self.driver.get(f'{self.live_server_url}/cart')
        self.assertTrue(len(self.driver.find_elements_by_xpath("//*[contains(text(), 'Comprar')]"))==0)
