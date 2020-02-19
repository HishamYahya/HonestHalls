from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('signup/', user_views.register, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('verify/', user_views.verify, name='verify'),
    path('verify-complete/<uidb64>/<token>/', user_views.verify_complete, name='verify-complete'),
    path('', user_views.profile, name='profile')
]
