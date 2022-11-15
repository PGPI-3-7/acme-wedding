from django.shortcuts import render

def metodo_pago_view(request):
    return render(request,'base/metodopago.html')
