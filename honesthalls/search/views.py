from django.shortcuts import redirect
from halls.models import Hall
from .forms import SearchForm
# Create your views here.


def searchbar(request):
    request.session['user_input'] = request.get('searchbar')
    return redirect(request, '/filter')
