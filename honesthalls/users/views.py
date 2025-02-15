from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from reviews.models import Review, ReviewPhotos, ReviewRating
from .models import Profile

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import verification_token
from django.core.mail import EmailMessage

from reviews.views import display_ratings, sort_reviews, user_ratings
import json


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Your account has been created!'
                             ' You are now able to login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if(request.method == 'POST'):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account details have '
                             'been updated.')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    user = request.user
    reviews = Review.objects.all().filter(user=user)
    review_ids = []
    for review in reviews:
        review_ids.append(review.id)
    ratings = ReviewRating.objects.filter(review__user = user)
    reviewratings = display_ratings(reviews, ratings)
    context = {
        'currentuser': request.user,
        'form': form,
        'profile': Profile.objects.get(user=user),
        'reviews': sort_reviews(reviews, reviewratings),
        'reviewphotos': ReviewPhotos.objects.filter(user=user),
        'reviewratings': reviewratings,
        'userratings': user_ratings(request, ratings),
        'review_ids': json.dumps(review_ids, separators=(',', ':'))
    }
    return render(request, 'users/profile.html', context)


@login_required
def password_change(request):
    if (request.method == 'POST'):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your password has been changed. '
                             'You can now log in with your new password.')
            return redirect('profile')
        else:
            messages.error(request, f'Please enter your current password, '
                           'and make sure the "New password" fields match.')
            return redirect('password-change')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'users/password_change.html', {'form': form})


@login_required
def verify(request):
    profile = Profile.objects.get(user=request.user)
    if profile.verified:
        messages.error(request, 'Account already verified.')
    else:
        domain = profile.user.email.split("@")[1]
        if domain != "manchester.ac.uk" and \
           domain != "postgrad.manchester.ac.uk" and \
           domain != "student.manchester.ac.uk":
            messages.error(request, 'Not a vaild university email account.')
        else:
            current_site = get_current_site(request)
            mail_subject = "Verify your HonestHalls account."
            uid = urlsafe_base64_encode(force_bytes(profile.user.pk))
            token = verification_token.make_token(profile)

            # Do not break the following string or the email will get cut off
            message = f"Hi {profile.user.first_name},\n\n You're receiving this email because you requested to verify your HonestHalls account.\n\n Please click on the following link to do so: http://{current_site.domain}/user/verify-complete/{uid}/{token} \n\n This is an automated email, please do not reply to this directly.\n\n\n Regards,\n The HonestHalls Team."

            # Old email:
            # message = f'http://{current_site.domain}/user/verify-complete/{uid}/{token}'

            email = EmailMessage(
                mail_subject, message, to=[profile.user.email]
            )
            email.send()

            messages.success(request, 'A verification email has been sent '
                             'to your account.')
    return redirect('profile')


def verify_complete(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    profile = Profile.objects.get(user__pk=uid)
    if profile.verified is not True:
        profile.verified = True
        profile.save()
        messages.success(request, 'Account has been verified.')
    return redirect('profile')
