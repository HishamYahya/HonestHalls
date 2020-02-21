from django.urls import path
from . import views
from django.contrib.auth import views as log_views

urlpatterns = [
    path('', views.search, name='search'),
]
