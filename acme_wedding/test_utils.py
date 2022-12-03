import datetime
from base.models import Category,Product

def create_product():
    test_category = Category()
    test_category.name = 'Test Category'
    test_category.slug = 'test-category'
    test_category.save()

    test_product = Product()
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