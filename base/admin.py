from django.contrib import admin
from .models import Category, Product, Incidence
from django import forms

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Incidence)
class IncidenceAdmin(admin.ModelAdmin):
    list_display = ['email', 'description']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated','amount']
    list_filter = ['available', 'created', 'updated', 'amount']
    list_editable = ['price', 'amount']
    prepopulated_fields = {'slug': ('name',)}
'''
class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'amount', 'category',
         'unidades']
         '''