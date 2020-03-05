from django.shortcuts import (
    render, reverse, redirect,
    Http404, HttpResponse, HttpResponseRedirect
)
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from halls.utils import render_form_errors
from users.models import Profile
from halls.models import Hall, RoomType
from reviews.models import Review, ReviewPhotos

from .forms import ReviewEditForm, ReviewPhotosEditForm
from django.forms import modelformset_factory

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
    if request.method == 'POST':
        form = ReviewEditForm(request.POST)
        if form.is_valid():
            # Add the needed references to the other models.
            form.instance.roomtype_id = int(form.cleaned_data.get('roomtype'))
            form.instance.user = request.user
            # Save to DB and print message.
            form.save()
            messages.success(
                request, "Your review was saved successfully. You can now add photos to it!")
            return redirect(reverse('review-edit', kwargs={'review_id': form.instance.id}))
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
        'profile': Profile.objects.get(user=request.user),
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
        'review': review,
        'form': form,
        'hall': hall,
        'roomtypes': roomtypes,
        'profile': Profile.objects.get(user=request.user),
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


@login_required
def review_photos(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.user_id != request.user.id:
        # The review is by a different user. Return to profile page.
        messages.error(
            request, "You can only delete reviews posted by yourself!")
        return HttpResponseRedirect(reverse('profile'))

    ReviewPhotosEditFormSet = modelformset_factory(
        ReviewPhotos, form=ReviewPhotosEditForm, extra=3)

    if request.method == 'POST':
        formset = ReviewPhotosEditFormSet(request.POST, request.FILES,
                                          queryset=ReviewPhotos.objects.none())
        if formset.is_valid():
            for form in formset.cleaned_data:
                if form:
                    image = form['photo_path']
                    reviewPhoto = ReviewPhotos(photo_path=image, photo_desc=form['photo_desc'],
                                               review=review, user=review.user)
                    reviewPhoto.save()
            messages.success(
                request, f'Your changes to review photos have been made.')
            request.method = 'GET'
            return redirect(reverse('review-edit', kwargs={'review_id': review.id}))

    else:
        formset = ReviewPhotosEditFormSet(queryset=ReviewPhotos.objects.none())

    context = {
        'formset': formset
    }

    return render(request, 'reviews/review-photos.html', context)

# function takes a list of reviews and a list of ratings for those reviews 
# and returns a dictionary of review ids and their associated ratings
def display_ratings(reviews, ratings):
    reviews_dic = {review.id: 0 for review in reviews} # set initial rating
    for rating in ratings:                           # for all reviews to 0
        if (rating.vote): # if rating is an upvote
            reviews_dic[rating.review.id] += 1 # add 1 to rating of that review
        else:
            reviews_dic[rating.review.id] -= 1 # sub 1 from rating of that review
    return reviews_dic

# function takes a list of reviews and a dictionary of review ids and their
# associated ratings and returns a list of sorted reviews based off of ratings
def sort_reviews(reviews, reviews_dic):
    # sort the dictionary of review ids based off of their ranking, highest to lowest
    sorted_review_ids = sorted(reviews_dic, key=reviews_dic.get, reverse=True)
    # create a dictionary so reviews can be obtained from their id
    reviews_with_ids = {review.id: review for review in reviews}
    sorted_reviews = []
    for review_id in sorted_review_ids: # iterate through sorted review ids
        sorted_reviews.append(reviews_with_ids[review_id]) # add the related review
    return sorted_reviews                                  # to sorted list

# function takes a request object and a list of review ratings and 
# returns a dictionary of review ids and the users ratings
def user_ratings(request, ratings):
    if request.user.is_authenticated: # check if a user is logged on
        reviews_rated = ratings.filter(user=request.user) # get users reviews
        # create a dictionary of review ids and how the user voted
        users_ratings = {rating.review.id: rating.vote for rating in reviews_rated}
        return users_ratings
    return {}


@login_required
def report(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.user_id == request.user.id:
        # The review is by the reporter.
        messages.error(
            request, "You cannot report your own reviews.")

