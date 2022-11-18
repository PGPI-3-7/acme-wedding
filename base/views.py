from django.shortcuts import render

def politica_envio_view(request):
    return render(request,'base/politicaenvio.html')