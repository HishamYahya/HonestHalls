from django.shortcuts import (
    render, reverse,
    Http404, HttpResponse, HttpResponseRedirect
)
from django.utils import timezone


def index(request):
    """ Serves the project homepage """
    context = {'server_time': timezone.now()}
    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'halls/index.html', context)


def hallpage(request):
    # Dummy data
    # For fully working version, we need to get this info from database
    context = {
        'title': 'Hall Page',
        'hallname': 'Hulme Hall',
        'campus': 'Victoria Park',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque at eros porta elit faucibus luctus. Maecenas justo massa, euismod in pulvinar in, accumsan a erat. Sed ac dui ipsum. Nulla dapibus viverra rutrum. Proin id felis at massa ornare tristique. Morbi turpis mauris, facilisis non dolor vel, gravida scelerisque mauris.',
        'catering': 'Catered',
        'location': 'linktomap.com',
    }
    return render(request, 'halls/hallpage.html', context)
