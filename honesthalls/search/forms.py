from django import forms

from halls.models import Hall

class SearchForm(forms.ModelForm):
    text = forms.CharField(min_length=0, max_length=2500)

    class Meta:
        model = Hall
        fields = ['text']
