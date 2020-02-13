from django.shortcuts import render
from .forms import *


def filter_view(request):
    # Dummy data currently being used
    halls = [
        {
            'name': 'Hall1',
            'isEnsuite': True,
            'isCatered' : False,
            'hasBasin' : False,
            'isSingle' : True,
            'isDouble' : False,
            'Campus' : '1'
        },
        {
            'name': 'Hall2',
            'isEnsuite': False,
            'isCatered' : True,
            'hasBasin' : True,
            'isSingle' : False,
            'isDouble' : True,
            'Campus' : '1'
        }
    ]

    # request.POST returns null if the form hasn't been submitted yet
    # It's used to tell the template to show all halls
    # the first time the page loads
    submitted = request.POST

    # Initilize filters
    # TODO: Add filter variables here
    isEnsuite = None
    isCatered = None
    hasBasin = None
    isSingle = None
    isDouble = None
    CampusList = '1'
    if(submitted):
        form = FilterForm(request.POST)
        if(form.is_valid()):
            # Get boolean value of checkbox
            # TODO: Assign here all the filter variables to
            # their respective values in the form
            isEnsuite = form.cleaned_data.get('isEnsuite')
            isCatered = form.cleaned_data.get('isCatered')
            hasBasin = form.cleaned_data.get('hasBasin')
            isSingle = form.cleaned_data.get('isSingle')
            isDouble = form.cleaned_data.get('isDouble')
            whichHall = form.cleaned_data.get('whichHall')
            CampusList = submitted.get('CampusList')

    else:
        form = FilterForm()
        CampusList = submitted.get('CampusList')

    # Pass the halls data and the filters to the template form.html
    context = {
        'form': form,
        'halls': halls,
        'isEnsuite': isEnsuite,
        'isCatered': isCatered,
        'hasBasin' : hasBasin,
        'isSingle' : isSingle,
        'isDouble': isDouble,
        'submitted': submitted,
        'CampusList': CampusList
    }
    return render(request, 'filter/form.html', context)
