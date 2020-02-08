from django import forms


class FilterForm(forms.Form):
    # TODO: Add fields here
    isEnsuite = forms.BooleanField(label='Ensuite? ', required=False)
