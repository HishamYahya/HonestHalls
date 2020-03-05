from django.shortcuts import render
from django.db.models import Q
from .forms import *
from halls.models import Hall, RoomType, HallPhotos
from difflib import SequenceMatcher
import string


def filter_view(request):
    # request.POST returns null if the form hasn't been submitted yet
    # It's used to tell the template to show all halls
    # the first time the page loads
    submitted = request.POST

    # String passed from search
    search_string = request.GET.get('searchbar')
    unique_halls = set()

    # TODO: results_rooms should only query the search results
    if (search_string is None):
        results_rooms = RoomType.objects.all()
    else:

        '''Here is the matching.'''

        results_rooms = RoomType.objects.filter(Q(hall__name__icontains=search_string))
        search_words = search_string.split()
        all_rooms = Hall.objects.all()
        matcher = []
        result_matcher = []
        num = 0
        for hall in all_rooms:
            matcher.append([])
            for i in range(3):
                matcher[num].append(0)
            num += 1
        count = 0
        for hall in all_rooms:
            num = 0
            record = False
            for i in range(len(search_words)):
                search_word = search_words[i]
                name = hall.name.split()
                text = hall.text.split()
                campus = hall.campus
                matcher[num][0], matcher[num][1], matcher[num][2] = 0, 0, 0
                ratio = 0
                for j in range(len(name)):
                    word = name[j]
                    if len(word) <= len(search_word):
                        ratio = SequenceMatcher(None, search_word, word).ratio()
                        if ratio > matcher[num][0]:
                            matcher[num][0] = ratio
                    else:
                        for count_1 in range(len(word) - len(search_word) + 1):
                            name_string = ""
                            for count_2 in range(len(search_word)):
                                name_string += word[count_1 + count_2]
                            ratio = SequenceMatcher(None, search_word, name_string).ratio()
                            if ratio > matcher[num][0]: matcher[num][0] = ratio
                ratio = 0
                for j in range(len(name)):
                    word = text[j]
                    if len(word) <= len(search_word):
                        ratio = SequenceMatcher(None, search_word, word).ratio()
                        if ratio > matcher[num][1]:
                            matcher[num][1] = ratio
                    else:
                        for count_1 in range(len(word) - len(search_word) + 1):
                            text_string = ""
                            for count_2 in range(len(search_word)):
                                text_string += word[count_1 + count_2]
                            ratio = SequenceMatcher(None, search_word, text_string).ratio()
                            if ratio > matcher[num][1]: matcher[num][1] = ratio
                campus_ratio = SequenceMatcher(None, search_word, campus).ratio()
                if campus_ratio > matcher[num][2]:
                    matcher[num][2] = campus_ratio
                if matcher[num][0] > 0.6 or matcher[num][1] > 0.8 or matcher[num][2] > 0.5 or record:
                    if not record:
                        record = True
                        result_matcher.append([])
                        result_matcher[count].append(hall.name)
                        result_matcher[count].append(1)
                        result_matcher[count].append(0)
                        result_matcher[count].append(0)
                    result_matcher[count][1] *= matcher[num][0]
                    result_matcher[count][2] += matcher[num][1]
                    result_matcher[count][3] = max(result_matcher[count][3], matcher[num][2])
                num += 1
            if record:
                count += 1

        """from here is the sorting"""
        sorting_data = []
        for i in range(len(result_matcher)):
            sorting_data.append([])
            print(result_matcher[i][0])
            sorting_data[i].append(result_matcher[i][0])
            sorting_data[i].append(max(result_matcher[i][1] * 100, result_matcher[i][2], result_matcher[i][3] * 10))

        for i in range(len(sorting_data)):
            for j in range(i+1, len(sorting_data)):
                if sorting_data[j][1] > sorting_data[i][1]:
                    tem = sorting_data[i][0]
                    sorting_data[i][0] = sorting_data[j][0]
                    sorting_data[j][0] = tem
                    tem = sorting_data[i][1]
                    sorting_data[i][1] = sorting_data[j][1]
                    sorting_data[j][1] = tem

        for c in range(count):
            results_rooms = RoomType.objects.filter(Q(hall__name__icontains = sorting_data[c][0]))
            for i in results_rooms:
                unique_halls.add(i.hall)
            for hall in unique_halls:
                hall.photos = list(HallPhotos.objects.filter(hall=hall))
        # TODO: Change so it only queries search results

    # A set is being used so it does not/cannot have duplicate halls

    if(submitted):
        form = FilterForm(request.POST)
        if(form.is_valid()):
            catered = form.cleaned_data.get('eat_options')
            basin_ensuite = form.cleaned_data.get('toilet_options')
            bedsize = form.cleaned_data.get('bed_options')
            campus = form.cleaned_data.get('campus_options')

            min_price = submitted.get('price1')
            max_price = submitted.get('price2')
            # Campus = submitted.get('Campus')

            # tries need to be seperate to allow only min price or only
            # max price to be used
            try:
                min_price = int(min_price) * 100
            except:
                min_price = None

            try:
                max_price = int(max_price) * 100
            except:
                max_price = None

            query = build_filter(catered, basin_ensuite, bedsize, campus,
                                 min_price, max_price)
            results_rooms = results_rooms.filter(*query)

    else:
        form = FilterForm()

    for i in results_rooms:
        unique_halls.add(i.hall)
        # only adds unique hall objects since unique_halls is a set

    # add image attribute to access in template
    for hall in unique_halls:
        hall.photos = list(HallPhotos.objects.filter(hall=hall))

    # Pass the halls data and filters to the template form.html
    context = {
        'form': form,
        'results_rooms': results_rooms,
        'results_halls': unique_halls,
    }

    return render(request, 'filter/form.html', context)


def build_filter(catered, basin_ensuite, bedsize, campus,
                 min_price, max_price):
    # ------- BUILDING THE QUERY ----------
    query = []
    # we use this to build up a query
    # this let's us choose the 'dont care' option
    # example query:
    # query = [Q(ensuite=isEnsuite), Q(catered=isCatered),
    # Q(basin=hasBasin), Q(bedsize__iexact=bedsize)]

    if basin_ensuite == 'basin':
        query.append(Q(basin=True))
    elif basin_ensuite == 'ensuite':
        query.append(Q(ensuite=True))
    elif basin_ensuite == 'neither':
        query.append(Q(basin=False))
        query.append(Q(ensuite=False))

    if campus != 'na':
        query.append(Q(hall__campus__iexact=campus))

    if bedsize != 'na':
        query.append(Q(bedsize__iexact=bedsize))

    if catered == 'self':
        query.append(Q(catered=False))
    elif catered == 'catered':
        query.append(Q(catered=True))

    # TODO: need to add appending query for price filter slider

    # ------------------ amend if slider is added -------------------
    # if both fields left empty
    if min_price is None and max_price is None:
        pass
    elif max_price is None:
        query.append(Q(price__gte=min_price))
    elif min_price is None:
        query.append(Q(price__lte=max_price))
    # if fields filled correctly
    elif min_price >= 0 and max_price >= 0 and min_price <= max_price:
        query.append(Q(price__range=(min_price, max_price)))
    else:
        pass
    # ---------------------------------------------------------------
    return query
