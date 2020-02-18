from django import forms

# FRUIT_CHOICES= [
#     ('orange', 'Oranges'),
#     ('cantaloupe', 'Cantaloupes'),
#     ('mango', 'Mangoes'),
#     ('honeydew', 'Honeydews'),
#     ]

# class UserForm(forms.Form):
#     first_name= forms.CharField(max_length=100)
#     last_name= forms.CharField(max_length=100)
#     email= forms.EmailField()
#     age= forms.IntegerField()
#     favorite_fruit= forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=FRUIT_CHOICES))

# key, value shown to user
BASIN_ENSUITE_NA = [
    ('ensuite', 'Ensuite'),
    ('basin', 'Basin'),
    ('neither', 'Neither')
    ]

class FilterForm(forms.Form):
    # TODO: Add fields here
    isEnsuite = forms.BooleanField(label='Ensuite ', required=False)
    hasBasin = forms.BooleanField(label='Basin ', required=False)
    toilet_options = forms.ChoiceField(choices = BASIN_ENSUITE_NA)
    isCatered = forms.BooleanField(label='Catered ', required=False)
    isSingle = forms.BooleanField(label='Single ', required=False)
    isDouble = forms.BooleanField(label='Double ', required=False)
