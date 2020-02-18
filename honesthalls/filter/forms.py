from django import forms

BEDSIZE_OPTIONS = [
    ('na', 'Don\'t care'),
    ('single', 'Single'),
    ('double', 'Double')
]

# key, value shown to user
BASIN_ENSUITE_NA = [
    ('na', 'Don\'t care'),
    ('neither', 'Neither'),
    ('ensuite', 'Ensuite'),
    ('basin', 'Basin')
    ]

CATERED = [
    ('na', 'Don\'t care'),
    ('self', 'Self-catered'),
    ('catered', 'Catered')
]

class FilterForm(forms.Form):
    # TODO: Add fields here
    #isEnsuite = forms.BooleanField(label='Ensuite ', required=False)
    #hasBasin = forms.BooleanField(label='Basin ', required=False)
    toilet_options = forms.ChoiceField(choices = BASIN_ENSUITE_NA)
    bed_options = forms.ChoiceField(choices = BEDSIZE_OPTIONS)
    eat_options = forms.ChoiceField(choices = CATERED)
    #isCatered = forms.BooleanField(label='Catered ', required=False)
    #isSingle = forms.BooleanField(label='Single ', required=False)
    #isDouble = forms.BooleanField(label='Double ', required=False)
