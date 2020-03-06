from django.urls import path
from . import views
from .forms import FormStepOne, FormStepTwo, FormStepThree

urlpatterns = [
    path('', views.quiz_view, name="quiz"),
    path('results/', views.results_view, name="results")
]
