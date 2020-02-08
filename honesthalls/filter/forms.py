from django import forms


class FilterForm(forms.Form):
    isEnsuite = forms.BooleanField(label='Ensuite? ', required=False)
