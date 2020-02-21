from django.shortcuts import render
from .forms import SearchForm
# Create your views here.

def search(request):
    form = SearchForm()
    context = {
        'form' : form
    }
    return render(request, 'search/search.html', context)