from django.urls import path
from . import views
from django.contrib.auth import views as log_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('', views.profile, name='profile'),
    
]
