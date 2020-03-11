from django.urls import path
from . import views
app_name="FAQ"

urlpatterns = [
	path('question_form/<int:hall_id>', views.question_form, name='question' )
]
