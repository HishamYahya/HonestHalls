from django.shortcuts import render, redirect
from halls.models import Hall, RoomType
from reviews.models import Review
from filter.views import build_filter


def quiz_view(request):
    return render(request, 'quiz/questions.html')

def results_view(request):
    # cleaning data
    answers=[]

    for key in request.GET:
        if len(request.GET[key]) == 1:
            answers.append(int(request.GET[key]))
    if(len(answers) < 3):
        return redirect('quiz')



    try:
        basin_ensuite = request.GET.get('basin_ensuite')
        catering = request.GET.get('catering')
        campus = request.GET.get('campus')
        bed = request.GET.get('bed')
    except:
        return redirect('quiz')


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

    for hall in all_halls:
        if(halls_avg[hall.name]["Number of reviews"] != 0):
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

    


    all_halls = Hall.objects.all()
    rooms = RoomType.objects.all()
    # repeated in case top one is deleted when code is replaced

    # put each hall in an object that has additional info
    class FilteredHall:
        def __init__(self, hall):
            self.messages = []
            self.fitsCriteria = True
            self.hall = hall
            self.name = hall.name
            self.text = hall.text
            self.filter()

        def filter(self):
            fitsToilet = False
            fitsBed = False
            fitsCatering = False

            for room in rooms:
                if(self.hall.name == room.hall.name):
                    if(room.catered and catering == 'catered'):
                        fitsCatering = True
                    if(not room.catered and catering == 'self-catered'):
                        fitsCatering = True

                    if(room.bedsize.lower() == bed):
                        fitsBed = True
                    if(room.ensuite and basin_ensuite == 'ensuite'):
                        fitsToilet = True
                    if(room.basin and basin_ensuite == 'basin'):
                        fitsToilet = True
            if(fitsBed):
                self.messages.append([True, bed.capitalize() + " beds"])
                # Give higher score if it fits criteria
                scores[self.name] = ((scores[self.name] * 4) + (scores[self.name] *2)) / 5
            else:
                self.fitsCriteria = False
                self.messages.append([False, 'No ' + bed + " beds"])

            if(fitsToilet):
                self.messages.append([True, basin_ensuite.capitalize() + " rooms"])
                # Give higher score if it fits criteria
                scores[self.name] = ((scores[self.name] * 4) + (scores[self.name] *2)) / 5
            else:
                self.fitsCriteria = False
                self.messages.append([False, 'No ' + basin_ensuite + " rooms"])
            if(fitsCatering):
                self.messages.append([True, catering.capitalize() + ' rooms'])
                scores[self.name] = ((scores[self.name] * 4) + (scores[self.name] *2)) / 5
            else:
                self.fitsCriteria = False
                self.messages.append([False, 'No ' + catering + ' rooms'])

    filtered_halls = {}
    for hall in all_halls:
        filtered_halls[hall.name] = FilteredHall(hall)

    results = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}

    form_halls = []
    for key in results:
        for hall in all_halls:
            if (key == hall.name):
                form_halls.append(filtered_halls[key])
                continue
    
    
    return render(request, 'quiz/results.html', {
        'form_data': form_halls,
    })


            