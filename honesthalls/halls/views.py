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

def index(request):
    """ Serves the project homepage """

 
    context = {'server_time': timezone.now()}
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
        'title': 'Hall Page',
        'hallname': 'Hulme Hall',
        'campus': 'Victoria Park',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque at eros porta elit faucibus luctus. Maecenas justo massa, euismod in pulvinar in, accumsan a erat. Sed ac dui ipsum. Nulla dapibus viverra rutrum. Proin id felis at massa ornare tristique. Morbi turpis mauris, facilisis non dolor vel, gravida scelerisque mauris.',
        'catering': 'Catered',
        'location': 'linktomap.com',
        'reviews' : Review.objects.all()
    }
    return render(request, 'halls/hallpage.html', context)
