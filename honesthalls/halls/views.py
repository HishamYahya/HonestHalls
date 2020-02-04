from django.shortcuts import render, reverse, Http404, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import Profile
from .validators import validate_email, validate_password, validate_username

# Serves the project homepage
def index(request):
    context = { 'server_time': timezone.now() }
    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'halls/index.html', context)

# User registration form
def user_signup(request):
    if request.method == 'GET':
        # Just serve the signup view.
        return render(request, 'halls/user/signup.html')
    elif request.method == 'POST':
        # Validate the data and create the user
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return HttpResponse('Passwords do not match!')

        try:
            validate_email(email)
            validate_username(username)
            validate_password(password1)
        except ValidationError as e:
            return HttpResponse(f'Validation Error: {e}')

        # TODO: Validate student email
        # TODO: Check if user already exists

        user = User(email=email, username=username)
        user.set_password(password1)
        user.save()

        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    else:
        return Http404();

# TODO: Add login view