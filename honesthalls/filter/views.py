from django.shortcuts import render
from django.db.models import Q
from .forms import *
from halls.models import Hall, RoomType, HallPhotos
from difflib import SequenceMatcher


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

        '''matcher records the ratio of similarity of the search function
         num refers to number which count the number all halls in database'''
        results_rooms = RoomType.objects.filter(Q(hall__name__icontains = search_string))
        all_rooms = Hall.objects.all()
        hall_data = []
        matcher = []
        num = 0
        text_ratio = 0
        name_ratio = 0
        campus_ratio = 0
        text_content = ''
        for hall in all_rooms:
            word_ratio = 0
            hall_data.append(hall.name)
            name_ratio = SequenceMatcher(None,search_string,hall.name).ratio()
            text_content = hall.text
            for word in text_content:
                word = word.rstrip()
                word_ratio = SequenceMatcher(None,search_string,word).ratio()
                if word_ratio > text_ratio: text_ratio = word_ratio
            campus_ratio = SequenceMatcher(None,search_string,hall.campus).ratio()
            matcher.append(max(name_ratio,text_ratio,campus_ratio))
            num += 1
        for c in range(num):
            if matcher[c] >= 0.8:
                results_rooms = RoomType.objects.filter(Q(hall__name__icontains = hall_data[c]))
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
