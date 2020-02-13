from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hall/<int:id>', views.hallpage, name='hallpage')
]
