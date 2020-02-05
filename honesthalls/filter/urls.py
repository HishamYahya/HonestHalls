from django.urls import path
from . import views

urlpatterns = [
    path('', views.filter_view, name='filter-page'),
]