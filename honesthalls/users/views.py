from django.shortcuts import (
    render, reverse,
    Http404, HttpResponse, HttpResponseRedirect
)
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, auth
from django.contrib.auth import login as django_login, authenticate
# from django.contrib.auth.decorator import login_required
from django.contrib import messages

from .models import Profile
from .forms import RegistrationForm, LoginForm


def signup(request):
    """ Handles user registration """
    if request.method == 'POST':
        # Validate the data and create the user
        form = RegistrationForm(request.POST)

        if form.data.get('password1') != form.data.get('password2'):
            messages.error(request, "The passwords don't match!")
            return render(request, 'users/signup.html')

        # Print all the errors
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

        # If there were validation errors
        # return early and show the form again
        if not form.is_valid():
            return render(request, 'users/signup.html', {'form': form})

        # TODO: Validate student email
        # TODO: Check if user already exists
        # TODO: Keep valid fields filled in when returning erronous signup form

        email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = User(email=email, username=username)
        user.set_password(password)
        user.save()

        # TODO: Login on signup
        # django_login(request, user)
        # messages.info(request, f'You are logged in as {username}')
        messages.info(request, f'Account created for {email}')
        return HttpResponseRedirect(reverse('index'))
    else:
        # Just serve the signup view.
        return render(request, 'users/signup.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User.objects.get(email__iexact=email)
            if user is None or not user.check_password(password):
                messages.error(request, f'Incorrect credentials!')
                return HttpResponseRedirect(reverse('login'))

            django_login(request, user)
            messages.info(request, f'You are logged in as {email}!')
            return HttpResponseRedirect(reverse('index'))
        else:
            # Print all the errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            # Return partially filled in form.
            return render(request, 'users/login.html', {'form': form})
    else:
        # Just serve the login view.
        return render(request, 'users/login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'users/logout.html')
