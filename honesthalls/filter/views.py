from django.shortcuts import render
from .forms import FilterForm


def filter_view(request):
    halls = [
        {
            'name': 'Hall1',
            'isEnsuite': True
        },
        {
            'name': 'Hall2',
            'isEnsuite': False
        }
    ]

    # request.POST returns null if the form hasn't been submitted yet
    # It's used to tell the template to show all halls
    # the first time the page loads
    submitted = request.POST

    # Initilize filters
    # TODO: Add filter variables here 
    isEnsuite = None

    if(submitted):
        form = FilterForm(request.POST)
        if(form.is_valid()):
            # Get boolean value of checkbox
            # TODO: Assign here all the filter variables to
            # their respective values in the form
            isEnsuite = form.cleaned_data.get('isEnsuite')
    else:
        form = FilterForm()

    # Pass the halls data and the filters to the template
    context = {
        'form': form,
        'halls': halls,
        'isEnsuite': isEnsuite,
        'submitted': submitted
    }
    return render(request, 'filter/form.html', context)