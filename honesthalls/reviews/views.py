from datetime import datetime, timedelta
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
from reviews.models import Review, ReviewPhotos, ReviewRating, Report


from .forms import ReviewEditForm, ReviewPhotosEditForm, ReportForm
from django.forms import modelformset_factory
from django.http import JsonResponse

from .forms import ReviewEditForm, ReviewPhotosEditFormSet, ReportForm

# Passed to the template to specify
# whether an existing review is being edited or a new one is being created.
REVIEW_WRITE_NEW = 'WRITE_NEW'
REVIEW_CHANGE_EXISTING = 'CHANGE_EXISTING'


@login_required
def write(request, hall_id):
    """ Allows the user to write a new review for a room. """
    conflicting_reviews = list(Review.objects.filter(
        user=request.user,
        date_created__gte=datetime.today() - timedelta(days=365),
    )[:1])

    if len(conflicting_reviews) > 0:
        cr = conflicting_reviews[0]
        cr_hall = cr.roomtype.hall.name
        cr_age = max(0, (datetime.today() - cr.date_created.replace(tzinfo=None)).days)
        messages.error(request, f"""
            Posting a second review in less than 365 days is disallowed.
            Your previous review of \"{cr_hall}\" was
            posted {cr_age} days ago.
        """)
        return redirect(f"{reverse('profile')}#review-{cr.id}")

    # We'll pass the hall to the view, so get the data needed for that
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
                request,
                "Your review was saved successfully. "
                "Now its time to add some photos!"
            )
            return redirect(reverse('review-photos', kwargs={'review_id': form.instance.id}))
        else:
            messages.error(
                request, "Please, correct any errors in the review form!")

    if request.method == 'GET':
        form = ReviewEditForm()
        users_reviews = Review.objects.filter(user=request.user)
        if len(users_reviews) > 4:
            messages.error(
                request, "You have exceeded the number of reviews an account can make. Please delete one of your reviews in order to make a new one.")
            return HttpResponseRedirect(reverse('hallpage', kwargs={'id': hall_id}))
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
    # get_card_data mainly adds photo and thumbnail
    hall = review.roomtype.hall.get_card_data()
    if request.method == 'POST':
        form = ReviewEditForm(request.POST, instance=review)
        if form.is_valid():
            # TODO: Check if valid
            review.roomtype_id = form.cleaned_data.get('roomtype')
            # Save to DB and print message.
            form.save()
            messages.success(
                request, "Your review was updated successfully!")

            if 'goto-photos' in request.POST:
                # The user pressed the save & edit photos button
                return redirect(reverse('review-photos', kwargs={'review_id': form.instance.id}))
        else:
            messages.error(
                request, "Please, correct any errors in the review form!")

    if request.method == 'GET':
        form = ReviewEditForm(model_to_dict(review))

    # Get the room types from the DB
    room_types = RoomType.objects.filter(hall_id=hall.get('id'))
    review_photos = review.reviewphotos_set.all()
    return render(request, 'reviews/review-edit.html', {
        'review': review,
        'review_photos': review.reviewphotos_set.all(),
        'form': form,
        'hall': hall,
        'roomtypes': room_types,
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

    if request.method == 'POST':
        # Delete the review from the DB and return to profile page.
        review.delete()
        messages.success(
            request, "Review deleted successfully!")
        return HttpResponseRedirect(reverse('profile'))
    else:
        # Send bad request for GET requests.
        return HttpResponse(status=400)


@login_required
def review_photos(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.user_id != request.user.id:
        # The review is by a different user. Return to profile page.
        messages.error(
            request, "You can only delete reviews posted by yourself!")
        return HttpResponseRedirect(reverse('profile'))

    if request.method == 'POST':
        formset = ReviewPhotosEditFormSet(
            request.POST,
            request.FILES,
            queryset=review.reviewphotos_set.none()
        )
        context = {
            'formset': formset,
            'review': review,
            'user': request.user,
        }
        if not formset.is_valid():
            for form in formset.forms:
                render_form_errors(request, form)
            return render(request, 'reviews/review-photos.html', context)
        else:
            for form in formset.forms:
                if form.cleaned_data:
                    # Call the overriden save() method to execute the
                    # action requested by the user.
                    form.save(user=request.user, review=review)
                    form.instance.refresh_from_db()
                    form['photo_path'].value = form.instance.photo_path
                    # form.fields['photo_path'].value = form.instance.photo_path

            messages.success(
                request, 'Your changes to review photos have been made.')
            return render(request, 'reviews/review-photos.html', context)

    else:
        formset = ReviewPhotosEditFormSet(
            queryset=review.reviewphotos_set.all())
        context = {
            'formset': formset,
            'review': review,
            'user': request.user,
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

def up_vote(request, hall_id, review_id):
    highlight = False
    review = Review.objects.filter(id=review_id)
    ratings = ReviewRating.objects.filter(review__id=review_id)
    if request.user.is_authenticated:
        user_rating = ratings.filter(user=request.user)
        if len(user_rating) == 0:
            new_rating = ReviewRating(review=review[0], user=request.user, vote=True)
            new_rating.save()
            highlight = True
        elif user_rating[0].vote == True:
            user_rating[0].delete()
        else:
            user_rating[0].vote = True
            user_rating[0].save()
            highlight = True
    ratings = ReviewRating.objects.filter(review__id=review_id)
    final_ratings = display_ratings(review, ratings)
    context = {
        'value': review_id,
        'logged_in': request.user.is_authenticated,
        'url': reverse("login"),
        'rating': final_ratings[review_id],
        'highlight_up': highlight,
        'highlight_down': False
    }
    return JsonResponse(context)

def down_vote(request, hall_id, review_id):
    highlight = False
    review = Review.objects.filter(id=review_id)
    ratings = ReviewRating.objects.filter(review__id=review_id)
    if request.user.is_authenticated:
        user_rating = ratings.filter(user=request.user)
        if len(user_rating) == 0:
            new_rating = ReviewRating(review=review[0], user=request.user, vote=False)
            new_rating.save()
            highlight = True
        elif user_rating[0].vote == False:
            user_rating[0].delete()
        else:
            user_rating[0].vote = False
            user_rating[0].save()
            highlight = True
    ratings = ReviewRating.objects.filter(review__id=review_id)
    final_ratings = display_ratings(review, ratings)
    context = {
        'value': review_id,
        'logged_in': request.user.is_authenticated,
        'url': reverse("login"),
        'rating': final_ratings[review_id],
        'highlight_up': False,
        'highlight_down': highlight
    }
    return JsonResponse(context)

@login_required
def report(request):
    review = get_object_or_404(Review, pk=review_id)

    if request.method == 'POST':
        form = ReportForm(request.POST)

        if form.is_valid():
            # Save to DB and print message.
            form.instance.review = review

            form.instance.user = request.user
            form.save()
            review.reported = True
            review.save()
            messages.success(
                request, "Your report was saved successfully!")
            return HttpResponseRedirect(reverse('report', kwargs={'review_id': review.id}))

        else:
            messages.error(
                request, "Please, correct any errors in the report form.")
            return render(request, 'reviews/report.html', {
                "form": form
            })
    else:
        form = ReportForm()
        return render(request, 'reviews/report.html', {
        "form": form
        })
