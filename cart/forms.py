from django import forms

class CartAddProductForm(forms.Form):
    override = forms.BooleanField(  required=False,
                                    initial=False,
                                    widget=forms.HiddenInput)