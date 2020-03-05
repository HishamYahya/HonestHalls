from django.shortcuts import render
from halls.models import Hall
from reviews.models import Review

def quiz_view(request):
    return render(request, 'quiz/questions.html')

def results_view(request):
    print(request.GET)
    # answers = [form.cleaned_data for form in form_list]
    # answers = [int(d["answer"]) for d in answers]
    answers = [1, 1, 3]
    # cleaning data
    
    # generating average for each hall (need to replace)
    all_halls = Hall.objects.all()
    all_reviews = Review.objects.all()
    halls_avg = {}
    for hall in all_halls:
        halls_avg[hall.name] = {
            "Cleanliness": 0,
            "Noise": 0,
            "Social Life": 0,
            "Facilities": 0,
            "Number of reviews": 0
        }
    
    for review in all_reviews:
        for hall in all_halls:
            if review.roomtype.hall ==  hall:
                halls_avg[hall.name]["Cleanliness"] += review.cleanliness
                halls_avg[hall.name]["Noise"] += review.noise
                halls_avg[hall.name]["Social Life"] += review.social_life
                halls_avg[hall.name]["Facilities"] += review.facilities
                halls_avg[hall.name]["Number of reviews"] += 1

    if(halls_avg[hall.name]["Number of reviews"] != 0):
        for hall in all_halls:
            halls_avg[hall.name]["Cleanliness"] /= halls_avg[hall.name]["Number of reviews"]
            halls_avg[hall.name]["Noise"] /= halls_avg[hall.name]["Number of reviews"]
            halls_avg[hall.name]["Social Life"] /= halls_avg[hall.name]["Number of reviews"]
            halls_avg[hall.name]["Facilities"] /= halls_avg[hall.name]["Number of reviews"]


    # algorithm
    scores = {}
    for key in halls_avg:
        cleanliness = halls_avg[key]['Cleanliness'] * (answers[0]/3)
        noise = halls_avg[key]['Noise'] * (answers[1]/3)
        social_life = halls_avg[key]['Social Life'] * (answers[2]/3)
        facilities = halls_avg[key]['Facilities'] * 2/3
        score = (cleanliness + noise + social_life + facilities) / 4
        scores[key] = score

    results = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}


    all_halls = Hall.objects.all()
    # repeated in case top one is deleted when code is replaced
    form_halls = []
    for key in results:
        for hall in all_halls:
            if (key == hall.name):
                form_halls.append(hall)
                continue

    return render(request, 'quiz/results.html', {
        'form_data': form_halls,
    })