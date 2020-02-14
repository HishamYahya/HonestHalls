from django import forms


class FilterForm(forms.Form):
    # TODO: Add fields here
    isEnsuite = forms.BooleanField(label='Ensuite ', required=False)
    isCatered = forms.BooleanField(label='Catered ', required=False)
    hasBasin = forms.BooleanField(label='Basin ', required=False)
    isSingle = forms.BooleanField(label='Single ', required=False)
    isDouble = forms.BooleanField(label='Double ', required=False)
