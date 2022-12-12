from django.utils.safestring import mark_safe
from django import forms
from .models import Order
from enum import Enum




class OrderCreateForm(forms.ModelForm):
    order_create = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    accept_terms = forms.BooleanField()
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city','remember','tipo_pago']

class RegisterOrderCreateForm(forms.ModelForm):
    user_order_create = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    remember_code = forms.CharField()
   
    class Meta:
        model = Order
        fields=['tipo_pago']
        