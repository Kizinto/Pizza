from django import forms

class PizzaForm(forms.Form):
    name = forms.CharField()
    price = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField(
        label='Select a Image',
        help_text='max. 10 megabytes'
    )