from django.shortcuts import (
    render, reverse,
    Http404, HttpResponse, HttpResponseRedirect
)
from django.utils import timezone
from django.shortcuts import get_object_or_404, get_list_or_404
from reviews.models import Review, ReviewPhotos, ReviewRating
from .models import Hall, RoomType, HallPhotos
from reviews.views import display_ratings, sort_reviews, user_ratings

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
    reviews = Review.objects.filter(roomtype__hall_id=id)
    ratings = ReviewRating.objects.filter(review__roomtype__hall__id = id)
    reviewratings = display_ratings(reviews, ratings)
    context = {
        'currentuser': request.user,
        'id': id,
        'hall': hall,
        'roomtypes': roomtypes,
        'hallphotos': hallphotos,
        'reviews': sort_reviews(reviews, reviewratings),
        'reviewphotos': ReviewPhotos.objects.filter(review__roomtype__hall_id=id),
        'reviewratings': reviewratings,
        'userratings': user_ratings(request, ratings)
    }
    return render(request, 'halls/hallpage.html', context)
