from django.shortcuts import render
from .forms import FormStepOne, FormStepTwo, FormStepThree
from formtools.wizard.views import SessionWizardView
from halls.models import Hall
from reviews.models import Review

class FormWizardView(SessionWizardView):
    template_name = "quiz/questions.html"
    form_list = [FormStepOne, FormStepTwo, FormStepThree]

    def done(self, form_list, **kwargs):
        answers = [form.cleaned_data for form in form_list]
        answers = [int(d["answer"]) for d in answers]
        # cleaning data
        
        # generating average for each hall (need to replace)
        all_halls = Hall.objects.all()
        all_reviews = Review.objects.all()
        halls = {}
        for hall in all_halls:
            halls[hall.name] = {
                "Cleanliness": 0,
                "Noise": 0,
                "Social Life": 0,
                "Facilities": 0,
                "Number of reviews": 0
            }
        
        for review in all_reviews:
            for hall in all_halls:
                if review.roomtype.hall ==  hall:
                    halls[hall.name]["Cleanliness"] += review.cleanliness
                    halls[hall.name]["Noise"] += review.noise
                    halls[hall.name]["Social Life"] += review.social_life
                    halls[hall.name]["Facilities"] += review.facilities
                    halls[hall.name]["Number of reviews"] += 1

        for hall in all_halls:
            halls[hall.name]["Cleanliness"] /= halls[hall.name]["Number of reviews"]
            halls[hall.name]["Noise"] /= halls[hall.name]["Number of reviews"]
            halls[hall.name]["Social Life"] /= halls[hall.name]["Number of reviews"]
            halls[hall.name]["Facilities"] /= halls[hall.name]["Number of reviews"]


        # algorithm
        scores = {}
        for key in halls:
            cleanliness = halls[key]['Cleanliness'] * (answers[0]/3)
            noise = halls[key]['Noise'] * (answers[1]/3)
            social_life = halls[key]['Social Life'] * (answers[2]/3)
            facilities = halls[key]['Facilities'] * 2/3
            score = (cleanliness + noise + social_life + facilities) / 4
            scores[key] = score



        print(halls)

        return render(self.request, 'quiz/results.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })
