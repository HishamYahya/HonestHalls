from django.shortcuts import render
from .forms import FilterForm


# Create your views here.
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
    submitted = request.POST
    isEnsuite = None
    if(submitted):
        form = FilterForm(request.POST)
        if(form.is_valid()):
            isEnsuite = form.cleaned_data.get('isEnsuite')
    else:
        form = FilterForm()
    context = {
        'form': form,
        'halls': halls,
        'isEnsuite': isEnsuite,
        'submitted': submitted
    }
    return render(request, 'filter/form.html', context)
