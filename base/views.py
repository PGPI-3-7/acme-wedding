from django.shortcuts import render

def datos_empresa_view(request):
    return render(request,'base/datosempresa.html')
