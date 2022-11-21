import random
from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def metodo_pago_view(request):
    return render(request,'base/metodopago.html')


def base(request):
    try:
        productos = random.sample(list(Product.objects.filter(available=True).values()),k=3)
    except:
        return render(request,'error.html',{'mensaje': 'Actualmente no hay suficientes productos disponibles como para mostrar el escaparate :('})
    return render(request,'inicio.html',{'p0':productos[0],'p1':productos[1],'p2':productos[2]})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'base/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug)


    return render(request,
                  'base/product/detail.html',
                  {'product': product})


def opciones_entrega_view(request):
    return render(request,'base/opcionesentrega.html')

def politica_envio_view(request):
    return render(request,'base/politicaenvio.html')

