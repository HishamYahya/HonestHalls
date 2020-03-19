from django.shortcuts import (
    render, reverse, redirect,
    Http404, HttpResponse, HttpResponseRedirect
)
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.urls import path

from halls.utils import render_form_errors

from django.forms import modelformset_factory
from django.http import JsonResponse


from .forms import QuestionForm
from halls.models import Hall

@login_required
def question_form(request, hall_id):
	hall = get_object_or_404(Hall, pk=hall_id)

	if request.method == 'POST':
		form = QuestionForm(request.POST)

		if form.is_valid():
			form.instance.hall = hall
			form.instance.user = request.user
			form.save()
			messages.success(
			request, "Your question was submitted.")
			return HttpResponseRedirect(reverse('hallpage', kwargs={'id': hall.id}))
		else:
			messages.error(
			request, "Questions must be no more than 200 characters.")
			return render(request, 'FAQ/question_form.html', {
			"form": form,
			"hall": hall
		})
	else:
		form = QuestionForm()
		return render(request, 'FAQ/question_form.html', {
		"form": form,
		"hall": hall
		})