from django.utils.safestring import mark_safe
from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    order_create = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    accept_terms = forms.BooleanField(label = mark_safe('He leído y acepto la <a href="/politicaprivacidad">política de privacidad</a> de Acme-wedding'))
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city','remember']

class RegisterOrderCreateForm(forms.ModelForm):
    user_order_create = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    remember_code = forms.CharField(label='Código de Verificación')
    class Meta:
        model = Order
        fields=[]
        