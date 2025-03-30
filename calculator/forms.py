from django import forms

class DistanceForm(forms.Form):
    source = forms.CharField(label='Endereço de Origem', max_length=255)
    destination = forms.CharField(label='Endereço de Destino', max_length=255)
