from django.urls import path
from . import views
from django.contrib.auth import views as log_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', log_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', log_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
