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

CAMPUSES = [
    ('na', 'Don\'t care'),
    ('fallowfield', 'Fallowfield'),
    ('victoria', 'Victoria Park'),
    ('city', 'City')
]

class FilterForm(forms.Form):
    # TODO: Add fields here
    toilet_options = forms.ChoiceField(choices = BASIN_ENSUITE_NA, label = "Toilet Options: ")
    bed_options = forms.ChoiceField(choices = BEDSIZE_OPTIONS, label = "Bedsize: ")
    eat_options = forms.ChoiceField(choices = CATERED, label = "Catering: ")
    campus_options = forms.ChoiceField(choices = CAMPUSES, label = "Campus: ")
