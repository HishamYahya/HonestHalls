from django.shortcuts import render
from .forms import FormStepOne, FormStepTwo
from formtools.wizard.views import SessionWizardView


class FormWizardView(SessionWizardView):
    template_name = "quiz/questions.html"
    form_list = [FormStepOne, FormStepTwo]

    def done(self, form_list, **kwargs):
        # cleaning data
        

        # algorithm

        return render(self.request, 'quiz/results.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
