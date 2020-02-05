from django.shortcuts import render

# Create your views here.
def filter_view(request):
    return render(request, 'filter/form.html')