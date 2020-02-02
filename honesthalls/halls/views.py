from django.shortcuts import render
from django.utils import timezone

# Serves the project homepage
def index(request):
    context = { 'server_time': timezone.now() }
    return render(request, 'halls/index.html', context)