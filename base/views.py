import random
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Incidence
from .forms import ProductForm, IncidenceForm
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
from django.contrib import messages
from django.core.mail import send_mail
from cart.forms import CartAddProductForm
from django.views.decorators.http import require_http_methods

def base(request):
    try:
        productos = random.sample(list(Product.objects.filter(available=True).values()),k=3)
    except:
        return render(request,'error.html',{'mensaje': 'Actualmente no hay suficientes productos disponibles como para mostrar el escaparate :('})
    return render(request,'inicio.html',{'p0':productos[0],'p1':productos[1],'p2':productos[2]})

@require_http_methods(["GET", "POST"])
def incidence(request):
    if request.method == 'POST':
        form = IncidenceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            correo = cd['email']
            desc = cd['description']
            incidence = Incidence(email=correo, description=desc)
            incidence.save()

            subject = f'Has recibido una evidencia'
            message = f'Hemos recibido por parte de ACME Wedding un problema a solucionar,\n\n' \
                        f'Para encontrar con la persona que encontró el error contactar: {correo}.\n' \
                        f'El problema es: {desc}.'
            send_mail(subject, message, 'acmewedding.elesemca@gmail.com', ['acmewedding.elesemca@gmail.com'])
            sent = True

            messages.success(request,'Tu problema se ha enviado correctamente. Muchas gracias :)')
        else:
            print('ERROR')
            messages.error(request,'Los datos introducidos no son válidos')
    else:
        form = IncidenceForm()
    return render(request,'incidence/incidencias.html',{'form':form})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(pk__in=set( Product.objects.all().values_list('category',flat=True) ))

    categories_limit=categories[0:3]
    categories_all=categories[3:]
    products_ava = Product.objects.filter(available=True)
    products_sol = Product.objects.filter(available=False)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_ava = products_ava.filter(category=category)
        products_sol = products_sol.filter(category=category)

    # Asigna un formulario a cada producto disponible
    products = {p:CartAddProductForm() for p in products_ava}

    return render(request,
                  'product/catalogo.html',
                  {'category': category,
                   'categories_limit': categories_limit,
                   'categories_all': categories_all,
                   'products': products,
                   'products_sol': products_sol
                   })

def product_detail(request, id, slug):
    if request.method=='GET':
        product = get_object_or_404(Product,
                                    id=id,
                                    slug=slug)
        cart_product_form = CartAddProductForm()

        admin = request.user.is_staff
        categories = Category.objects.exclude(name = product.category)
        
        
        return render(request,'product/detail.html',
                    {'product': product,
                    'admin': admin,
                    'categories': categories,
                    'cart_product_form':cart_product_form})

    elif request.method=='POST':
        form = ProductForm(request.POST,request.FILES)
        product = Product.objects.get(id=id)
        admin = request.user.is_staff
        categories = Category.objects.exclude(name = product.category)
        if form.is_valid():
            name=form.data['name']
            
            if name!='': 
                product.name = name
                product.slug=slugify(form.data['name'])
            else:
                messages.error(request,'Introduce un nombre válido')
                return render(request,'product/detail.html',
                    {'product': product,
                    'admin': admin,
                    'categories': categories})
            
            
            categoria = Category.objects.get(name=form.data['category'])
            product.category = categoria
            
            amount= int(form.data['amount'])
            if amount != None and amount>=0: 
                product.amount = int(form.data['amount'])
            else:
                messages.error(request,'Introduce una cantidad positiva (mayor o igual que 0)')
                return render(request,'product/detail.html',
                    {'product': product,
                    'admin': admin,
                    'categories': categories})
            
            precio= float(form.data['price'])
            if precio != None and precio>=0: 
                product.price = form.data['price']
            else:
                messages.error(request,'Introduce un precio positivo (mayor o igual que 0)')
                return render(request,'product/detail.html',
                    {'product': product,
                    'admin': admin,
                    'categories': categories})

            product.description = form.data['description']

            '''para que coja bien la imagen'''
            if request.FILES:
                imagen=str(request.FILES['image'])
                if(imagen.endswith('.jpg') or imagen.endswith('.png') ):
                    product.image=request.FILES['image']
                else:
                    messages.error(request,'Introduce una imagen válida (.png, .jpg)')
                    return render(request,'product/detail.html',
                        {'product': product,
                        'admin': admin,
                        'categories': categories})

            product.description = form.data['description']                 
            
            product.save()      

        
        return  HttpResponseRedirect('/producto/{}/{}/'.format(id,product.slug))

def metodo_pago_view(request):
    return render(request,'metodopago.html')
    
def opciones_entrega_view(request):
    return render(request,'opcionesentrega.html')

def politica_envio_view(request):
    return render(request,'politicaenvio.html')

def datos_empresa_view(request):
    return render(request,'datosempresa.html')

def terminos_uso_view(request):
    return render(request,'terminosuso.html')