from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


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

ACCESSIBLE = [
    ('na', 'Show all results'),
    ('accessible', 'Only search for accessible halls'),
]


class FilterForm(forms.Form):
    # TODO: Add fields here
    toilet_options = forms.ChoiceField(choices=BASIN_ENSUITE_NA,
                                       label="Toilet Options: ")
    bed_options = forms.ChoiceField(choices=BEDSIZE_OPTIONS, label="Bedsize: ")
    eat_options = forms.ChoiceField(choices=CATERED, label="Catering: ")
    campus_options = forms.ChoiceField(choices=CAMPUSES, label="Campus: ")
    accessible_options = forms.ChoiceField(choices=ACCESSIBLE, label="Results: ")
    min_price = forms.IntegerField(initial=None, required=False)
    max_price = forms.IntegerField(initial=None, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'toilet_options',
            'bed_options',
            'eat_options',
            'campus_options',
            'accessible_options',
            Row(
                Column('min_price', css_class='form-group col-md-6 mb-0'),
                Column('max_price', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Search')
        )
