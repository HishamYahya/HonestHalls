from django.shortcuts import (
    render, reverse,
    Http404, HttpResponse, HttpResponseRedirect
)
from django.utils import timezone
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Hall, RoomType, HallPhotos, Review


def index(request):
    """ Serves the project homepage """
    # values() gets dicts instead of instances
    # which we can extend before passing to the view
    sample_halls = [hall.get_card_data() for hall in Hall.objects.all()[:5]]

    context = {
        'server_time': timezone.now(),
        'sample_halls': sample_halls
    }

    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'halls/index.html', context)


def hallpage(request, id):
    hall = get_object_or_404(Hall, pk=id)
    roomtypes = hall.roomtype_set.all()
    hallphotos = hall.hallphotos_set.all()
    context = {
        'id': id,
        'hall': hall,
        'roomtypes': roomtypes,
        'hallphotos': hallphotos,
        'reviews' : Review.objects.all()
    }
    return render(request, 'halls/hallpage.html', context)
