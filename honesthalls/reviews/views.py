from django.shortcuts import (
    render, reverse,
    Http404, HttpResponse, HttpResponseRedirect
)
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from halls.utils import render_form_errors
from halls.models import Hall
from reviews.models import Review, RoomType

from .forms import ReviewEditForm

# Passed to the template to specify
# whether an existing review is being edited or a new one is being created.
REVIEW_WRITE_NEW = 'WRITE_NEW'
REVIEW_CHANGE_EXISTING = 'CHANGE_EXISTING'


@login_required
def write(request, hall_id):
    """ Allows the user to write a new review for a room. """
    # We'll pass the hall to the view, so get the data needed for that
    # get_card_data mainly adds main_photo
    hall = get_object_or_404(Hall, pk=hall_id)
    hall_data = hall.get_card_data()
    # TODO: Verify whether the user is allowed to post this review.

    if request.method == 'POST':
        form = ReviewEditForm(request.POST)
        if form.is_valid():
            # Add the needed references to the other models.
            form.instance.roomtype_id = int(form.cleaned_data.get('roomtype'))
            form.instance.user = request.user
            # Save to DB and print message.
            form.save()
            messages.success(
                request, "Your review was saved successfully!")
            # We then allow the user to edit the review futher.
            return HttpResponseRedirect(reverse(
                'review-edit',
                kwargs={'review_id': form.instance.id}
            ))
        else:
            messages.error(
                request, "Please, correct any errors in the review form!")

    if request.method == 'GET':
        form = ReviewEditForm()

    roomtypes = hall.roomtype_set.all()
    return render(request, 'reviews/review-edit.html', {
        'form': form,
        'hall': hall_data,
        'roomtypes': roomtypes,
        'user': request.user,
        'mode': REVIEW_WRITE_NEW
    })


@login_required
def edit(request, review_id):
    """ Allows the user to edit an existing review. """
    review = get_object_or_404(Review, pk=review_id)
    if review.user_id != request.user.id:
        messages.error(
            request, "You can only edit reviews posted by yourself!")
        return HttpResponseRedirect(reverse('index'))

    # We'll pass the hall to the view, so get the data needed for that
    # get_card_data mainly adds main_photo
    hall = review.roomtype.hall.get_card_data()
    if request.method == 'POST':
        form = ReviewEditForm(request.POST, instance=review)
        if form.is_valid():
            # TODO: Check if valid
            review.roomtype_id = form.cleaned_data.get('roomtype')
            # Save to DB and print message.
            form.save()
            messages.success(
                request, "Your review was saved successfully!")
        else:
            messages.error(
                request, "Please, correct any errors in the review form!")

    if request.method == 'GET':
        form = ReviewEditForm(model_to_dict(review))

    # Get the room types from the DB
    roomtypes = RoomType.objects.filter(hall_id=hall.get('id'))
    return render(request, 'reviews/review-edit.html', {
        'form': form,
        'hall': hall,
        'roomtypes': roomtypes,
        'user': request.user,
        'date_created': review.date_created,
        'date_modified': review.date_modified,
        'mode': REVIEW_CHANGE_EXISTING
    })


@login_required
def delete(request, review_id):
    """ Allows the user to delete an existing review. """
    review = get_object_or_404(Review, pk=review_id)
    if review.user_id != request.user.id:
        # The review is by a different user. Return to profile page.
        messages.error(
            request, "You can only delete reviews posted by yourself!")
        return HttpResponseRedirect(reverse('profile'))

    # Delete the review from the DB and return to profile page.
    review.delete()
    messages.success(
        request, "Review deleted successfully!")
    return HttpResponseRedirect(reverse('profile'))
