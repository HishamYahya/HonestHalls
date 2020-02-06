from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hallpage/', views.hallpage, name = 'halls-hallpage')
]