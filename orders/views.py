from django.shortcuts import render
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm, RegisterOrderCreateForm
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404


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

                subject = f'Pedido num. {order.id}'
                message = f'Querido {order.first_name},\n\n' \
                          f'Su pedido ha sido registrado exitosamente.\n' \
                          f'El identificador de su pedido es: {order.id}.'
                send_mail(subject, message, 'acmewedding.elesemca@gmail.com', [order.email])
                sent = True

                if order.remember == True:
                    subject = f'Código de Verificación para Acme Wedding'
                    message = f'Querido {order.first_name},\n\n' \
                            f'Su código de verificación ha sido creado exitosamente.\n' \
                            f'El código de verificación es:  {order.remember_code}'
                    send_mail(subject, message, 'acmewedding.elesemca@gmail.com', [order.email])
                    sent = True


                return render(request,
                            'orders/order/created.html',
                            {'order': order})
                            
        if 'user_order_create' in request.POST:
            form = RegisterOrderCreateForm(request.POST)
            if form.is_valid():
                if(len(Order.objects.filter(remember_code=form.data['remember_code'])))>0:
                    aux_order = Order.objects.get(remember_code=form.data['remember_code'])
                    order=Order(
                        first_name=aux_order.first_name,
                        last_name=aux_order.last_name,
                        email=aux_order.email,
                        address=aux_order.email,
                        postal_code=aux_order.postal_code,
                        city=aux_order.city)
                    order.save()
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

                subject = f'Pedido num. {order.id}'
                message = f'Querido {order.first_name},\n\n' \
                          f'Su pedido ha sido registrado exitosamente.\n' \
                          f'El identificador de su pedido es: {order.id}.'
                send_mail(subject, message, 'acmewedding.elesemca@gmail.com', [order.email])
                sent = True


                return render(request,
                            'orders/order/created.html',
                            {'order': order})

    else:
        form = OrderCreateForm()
        form2= RegisterOrderCreateForm() 
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form, 'form2': form2})