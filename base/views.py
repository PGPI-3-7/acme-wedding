from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products_ava = Product.objects.filter(available=True)
    products_sol = Product.objects.filter(available=False)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_ava = products_ava.filter(category=category)
        products_sol = products_sol.filter(category=category)
    return render(request,
                  'base/product/list2.html',
                  {'category': category,
                   'categories': categories,
                   'products': products_ava,
                   'products_sol': products_sol
                   })


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)


    return render(request,
                  'shop/product/detail.html',
                  {'product': product})
