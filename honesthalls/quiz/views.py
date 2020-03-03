from django.shortcuts import render
from .forms import FormStepOne, FormStepTwo, FormStepThree
from formtools.wizard.views import SessionWizardView


class FormWizardView(SessionWizardView):
    template_name = "quiz/questions.html"
    form_list = [FormStepOne, FormStepTwo, FormStepThree]

    def done(self, form_list, **kwargs):
        answers = [form.cleaned_data for form in form_list]
        answers = [int(d["answer"]) for d in answers]
        # cleaning data
        

        # algorithm
        scores = {}
        for key in halls:
            cleanliness = halls[key]['Cleanliness'] * (answers[0]/3)
            noise = halls[key]['Noise'] * (answers[1]/3)
            social_life = halls[key]['Social Life'] * (answers[2]/3)
            facilities = halls[key]['Facilities'] * 2/3
            score = (cleanliness + noise + social_life + facilities) / 4
            scores[key] = score


        return render(self.request, 'quiz/results.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
