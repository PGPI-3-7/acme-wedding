import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from django.core.mail import send_mail


# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            for item in order.items.all():
                product = item.product
                product.amount = product.amount - item.quantity
                product.save()
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # launch asynchronous task
            
            subject = f'Pedido realizado correctamente'
            message = f'Querido {order.first_name},\n\n' \
                    f'Su pedido ha sido registrado exitosamente.\n' \
                    f'El identificador de su pedido es: {order.id}'
            send_mail(subject, message, 'acmewedding.elesemca@gmail.com', [order.email])
            sent = True

            if order.remember==True:
                subject = f'Código de Verificación para Acme Wedding'
                message = f'Querido {order.first_name},\n\n' \
                        f'Su código de verificación ha sido creado exitosamente.\n' \
                        f'El código de verificación es:  {order.remember_code}'
                send_mail(subject, message, 'acmewedding.elesemca@gmail.com', [order.email])
                sent = True

            return render(request,
                            'orders/order/created.html',
                            {'order': order})
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):

    return render(request, 'orders/created.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')