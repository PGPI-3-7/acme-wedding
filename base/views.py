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
    cat = Category.objects.all()
    categories=[]
    for c in cat:
        if len(Product.objects.filter(category=c))>0:
            categories.append(c)

    categories_limit=categories[0:3]
    categories_all=categories[3:]
    products_ava = Product.objects.filter(available=True)
    products_sol = Product.objects.filter(available=False)
    print(Product.objects.all().values())
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_ava = products_ava.filter(category=category)
        products_sol = products_sol.filter(category=category)
    return render(request,
                  'product/catalogo.html',
                  {'category': category,
                   'categories_limit': categories_limit,
                   'categories_all': categories_all,
                   'products': products_ava,
                   'products_sol': products_sol
                   })


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug)


    return render(request,
                  'product/detail.html',
                  {'product': product})


def opciones_entrega_view(request):
    return render(request,'base/opcionesentrega.html')

def politica_envio_view(request):
    return render(request,'base/politicaenvio.html')

def datos_empresa_view(request):
    return render(request,'base/datosempresa.html')

