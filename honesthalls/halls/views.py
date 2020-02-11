from django.shortcuts import (
    render, reverse,
    Http404, HttpResponse, HttpResponseRedirect
)
from django.utils import timezone
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Hall, RoomType


def index(request):
    """ Serves the project homepage """
    context = {'server_time': timezone.now()}
    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'halls/index.html', context)


def hallpage(request, id):
    hall = get_object_or_404(Hall, pk=id)
    roomtypes = hall.roomtype_set.all()
    context = {
        'id': id,
        'hall': hall,
        'roomtypes': roomtypes,
    }
    return render(request, 'halls/hallpage.html', context)
