from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(label='name')
    amount = forms.IntegerField(label='amount')
    category = forms.CharField(label='category')
    description = forms.CharField(label='description')
    price = forms.FloatField(label='price')
    #image = forms.ImageField(label='image')

class IncidenceForm(forms.Form):
    email = forms.EmailField(label="correo")
    description = forms.CharField(label="description")
