from django.shortcuts import (
    render, reverse,
    Http404, HttpResponse, HttpResponseRedirect
)
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

from .models import Profile
from .forms import RegistrationForm


def index(request):
    """ Serves the project homepage """
    context = {'server_time': timezone.now()}
    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'halls/index.html', context)


def user_signup(request):
    """ Handles user registration """
    if request.method == 'POST':
        # Validate the data and create the user
        form = RegistrationForm(request.POST)

        if form.data.get('password1') != form.data.get('password2'):
            messages.error(request, "The passwords don't match!")
            return render(request, 'halls/user/signup.html')

        # Print all the errors
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

        # If there were validation errors
        # return early and show the form again
        if not form.is_valid():
            return render(request, 'halls/user/signup.html', {'form': form})

        # TODO: Validate student email
        # TODO: Check if user already exists

        email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = User(email=email, username=username)
        user.set_password(password)
        user.save()

        login(request, user)
        messages.info(request, f'You are logged in as {username}')
        return reverse('index')
    else:
        # Just serve the signup view.
        return render(request, 'halls/user/signup.html')

# TODO: Add login view
