from django.urls import path, include
from . import views

app_name = 'base'

urlpatterns = [
    path('',views.base),
    path('catalogo', views.product_list, name='product_list'),
    path('catalogo/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('producto/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('incidencias',views.incidence, name="incidence_list"),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('politicaprivacidad/', views.politica_privacidad, name='politica_privacidad'),

]