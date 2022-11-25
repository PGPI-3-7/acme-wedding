from django.shortcuts import render
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm, RegisterOrderCreateForm
from .tasks import order_created, verification_code_created
from django.contrib import messages


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        
        if 'order_create' in request.POST:
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save()
                for item in cart:
                    OrderItem.objects.create(order=order,
                                            product=item['product'],
                                            price=item['price'],
                                            quantity=item['quantity'])
                # clear the cart
                cart.clear()
                # launch asynchronous task
                order_created.delay(order.id)
                verification_code_created(order.remember_code)
                return render(request,
                            'orders/order/created.html',
                            {'order': order})
                            
        if 'user_order_create' in request.POST:
            form = RegisterOrderCreateForm(request.POST)
            if form.is_valid():
                if(len(Order.objects.filter(remember_code=form.data['user_order_create'])))>0:
                    aux_order = Order.objects.get(remember_code=form.data['user_order_create'])
                    order=Order(
                        first_name=aux_order.first_name,
                        last_name=aux_order.last_name,
                        email=aux_order.email,
                        address=aux_order.email,
                        postal_code=aux_order.postal_code,
                        city=aux_order.city)
                else:
                    messages.error(request,'Introduce un nombre válido')
                    form = OrderCreateForm()
                    form2= RegisterOrderCreateForm() 
                    return render(request,
                                  'orders/order/create.html',
                                  {'cart': cart, 'form': form, 'form2': form2})
                

                for item in cart:
                    OrderItem.objects.create(order=order,
                                            product=item['product'],
                                            price=item['price'],
                                            quantity=item['quantity'])
                # clear the cart
                cart.clear()
                # launch asynchronous task
                order_created.delay(order.id)
                return render(request,
                            'orders/order/created.html',
                            {'order': order})

    else:
        form = OrderCreateForm()
        form2= RegisterOrderCreateForm() 
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form, 'form2': form2})