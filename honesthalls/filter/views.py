from django.shortcuts import render
from django.db.models import Q
from .forms import *
from halls.models import Hall, RoomType, HallPhotos


def filter_view(request):
    # request.POST returns null if the form hasn't been submitted yet
    # It's used to tell the template to show all halls
    # the first time the page loads
    submitted = request.POST

    # Initilize filters
    # TODO: Add filter variables here
    search = None

    results_rooms = RoomType.objects.all()
    unique_halls = set()
    # A set is being used so it does not/cannot have duplicate halls

    if(submitted):
        form = FilterForm(request.POST)
        if(form.is_valid()):
            search = submitted.get('search')

            catered = form.cleaned_data.get('eat_options')
            basin_ensuite = form.cleaned_data.get('toilet_options')
            bedsize = form.cleaned_data.get('bed_options')
            campus = form.cleaned_data.get('campus_options')


            min_price = submitted.get('price1')
            max_price = submitted.get('price2')
            #Campus = submitted.get('Campus')

            # tries need to be seperate to allow only min price or only max price to be used
            try:
                min_price = int(min_price) * 100
            except:
                min_price = None

            try:
                max_price = int(max_price) * 100
            except:
                max_price = None


            # ------- BUILDING THE QUERY ----------
            query = []
            # we use this to build up a query
            # this lets us choose the 'dont care' option
            # example query:
            # query = [Q(ensuite=isEnsuite), Q(catered=isCatered), Q(basin=hasBasin), Q(bedsize__iexact=bedsize)]


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

            # TODO: need to add appending query for price filter 

            # ------ hisham delete this once you're done --------------------------------------------------
            if min_price == None and max_price == None: # if both fields left empty
                # results_rooms = RoomType.objects.filter(ensuite=isEnsuite, catered=isCatered, basin=hasBasin, bedsize__iexact=bedsize)
                pass
            elif max_price == None:
                query.append(Q(price__gte=min_price))
                #results_rooms = RoomType.objects.filter(ensuite=isEnsuite, catered=isCatered, basin=hasBasin, bedsize__iexact=bedsize, price__gte=min_price)
            elif min_price == None:
                query.append(Q(price__lte=max_price))
                #results_rooms = RoomType.objects.filter(ensuite=isEnsuite, catered=isCatered, basin=hasBasin, bedsize__iexact=bedsize, price__lte=max_price)
            elif min_price >= 0 and max_price >= 0 and min_price <= max_price: # if fields filled correctly
                query.append(Q(price__range=(min_price, max_price)))
                #results_rooms = RoomType.objects.filter(ensuite=isEnsuite, catered=isCatered, basin=hasBasin, bedsize__iexact=bedsize, price__range=(min_price, max_price))
            else:
                pass
                #results_rooms = RoomType.objects.filter(ensuite=isEnsuite, catered=isCatered, basin=hasBasin, bedsize__iexact=bedsize)
            # -------------------------------------------------------------------------------------------

            results_rooms = RoomType.objects.filter(*query)

            for i in results_rooms:
                unique_halls.add(i.hall)
                # only adds unique hall objects since unique_halls is a set


    else:
        form = FilterForm()
        for i in results_rooms:
            unique_halls.add(i.hall)
    
    # add image attribute to access in template
    for hall in unique_halls:
        hall.photos = list(HallPhotos.objects.filter(hall=hall))

    # Pass the halls data and the filters to the template form.html
    context = {
        'form': form,
        'results_rooms': results_rooms,
        'results_halls': unique_halls,
        'search': search,
    }

    return render(request, 'filter/form.html', context)
