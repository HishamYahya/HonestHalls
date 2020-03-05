from django.urls import path
from . import views
from .forms import FormStepOne, FormStepTwo, FormStepThree

urlpatterns = [
    path('', views.FormWizardView.as_view([FormStepOne, FormStepTwo, FormStepThree]), name="quiz")
]
