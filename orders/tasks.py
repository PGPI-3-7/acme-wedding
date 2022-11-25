from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent

@task
def verification_code_created(user_remember_code):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(remember_code=user_remember_code)
    subject = f'Código de Verificación para Acme Wedding'
    message = f'Querido {order.first_name},\n\n' \
              f'Su código de verificación ha sido creado exitosamente.' \
              f'El código de verificación es:  {order.remember_code}.'
    mail_sent = send_mail(subject,
                          message,
                          'v erificacion@acmewedding.com',
                          [order.email])
    return mail_sent