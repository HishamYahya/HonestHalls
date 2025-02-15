from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views


urlpatterns = [
    path('signup/', user_views.register, name='signup'),
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='logout'),

    path('verify/', user_views.verify, name='verify'),
    path('verify-complete/<uidb64>/<token>/', user_views.verify_complete,
         name='verify-complete'),

    path('', user_views.profile, name='profile'),

    path('password-change/', user_views.password_change,
         name='password-change'),

    path('password-reset/', auth_views.PasswordResetView.as_view
         (template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view
         (template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view
         (template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view
         (template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]

