from django import forms

OPTIONS = [
    (1, 'Not Important'),
    (2, 'I don\'t care'),
    (3, 'Important')
]

class FormStepOne(forms.Form):
    answer = forms.CharField(label='How important is cleanliness for you?', widget=forms.RadioSelect(choices=OPTIONS))

class FormStepTwo(forms.Form):
    answer = forms.CharField(label='How light of a sleeper are you?', widget=forms.RadioSelect(choices=[
        (1, 'Not at all'),
        (2, 'Somewhat'),
        (3, 'Need complete silence')  
    ]))

class FormStepThree(forms.Form):
    answer = forms.CharField(label='How important is social life for you?', widget=forms.RadioSelect(choices=OPTIONS))
