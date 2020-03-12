from django import forms
from django.forms import modelformset_factory

from FAQ.models import Questions

class QuestionForm(forms.ModelForm):
	question = forms.CharField(max_length=200)

	class Meta:
		model = Questions
		fields = ['question']