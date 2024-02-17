from django import forms

class inputsForm(forms.Form):
    link = forms.CharField(max_length=1000)