from django import forms

OPTIONS = [
    (1, 'Not Important'),
    (2, 'I don\'t care'),
    (3, 'Important')
]

class FormStepOne(forms.Form):
    answer = forms.CharField(label='How important is 1 for you?', widget=forms.RadioSelect(choices=OPTIONS))

class FormStepTwo(forms.Form):
    answer = forms.CharField(label='How important is 1 for you?', widget=forms.RadioSelect(choices=OPTIONS))