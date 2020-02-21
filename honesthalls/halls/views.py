from django.shortcuts import (
    render, reverse,
    Http404, HttpResponse, HttpResponseRedirect
)
from django.utils import timezone
from django.shortcuts import get_object_or_404, get_list_or_404
from reviews.models import Review
from .models import Hall, RoomType, HallPhotos


def index(request):
    """ Serves the project homepage """
    # Get a number of halls
    sample_halls = Hall.objects.all()[:5]
    # Convert them to dicts and add extras (eg. main_image).
    sample_halls = [hall.get_card_data() for hall in sample_halls]

    context = {
        'server_time': timezone.now(),
        'sample_halls': sample_halls
    }
    if request.user.is_authenticated:
        context['email'] = request.user.email

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
        'reviews': Review.objects.filter(roomtype__hall_id=id)
        # 'reviewphotos': ReviewPhotos.objects.filter(review__hall__id=id)
    }

    return render(request, 'halls/hallpage.html', context)
