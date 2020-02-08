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
