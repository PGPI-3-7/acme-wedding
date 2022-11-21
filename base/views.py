from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import ProductForm
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
from django.contrib import messages




def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    if request.method=='GET':
        product = get_object_or_404(Product,
                                    id=id,
                                    slug=slug)
        
        admin = request.user.is_staff
        categories = Category.objects.exclude(name = product.category)
        
        
        return render(request,'product/detail.html',
                    {'product': product,
                    'admin': admin,
                    'categories': categories})

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

    
    
