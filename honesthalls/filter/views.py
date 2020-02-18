from django.shortcuts import render
from django.db.models import Q
from .forms import *
from halls.models import Hall, RoomType


def filter_view(request):
    # Dummy data currently being used
    # halls = [
    #     {
    #         'name': 'Hall1',
    #         'isEnsuite': True,
    #         'isCatered' : False,
    #         'hasBasin' : False,
    #         'isSingle' : True,
    #         'isDouble' : False,
    #         'price': 1000,
    #         'Campus' : 'Fallowfield'
    #     },
    #     {
    #         'name': 'Hall2',
    #         'isEnsuite': False,
    #         'isCatered' : True,
    #         'hasBasin' : True,
    #         'isSingle' : False,
    #         'isDouble' : True,
    #         'price': 2000,
    #         'Campus' : 'Fallowfield'
    #     }
    # ]
    

    # request.POST returns null if the form hasn't been submitted yet
    # It's used to tell the template to show all halls
    # the first time the page loads
    submitted = request.POST

    # Initilize filters
    # TODO: Add filter variables here
    search = None
    # isEnsuite = None
    # isCatered = None
    # hasBasin = None
    # isSingle = None
    # isDouble = None
    # price1, price2 = 0, 0
    # Campus = None

    #^ do we need this???

    #results_halls = results_rooms.distinct('hall_id')
    #results_halls = Hall.objects.all()
    results_rooms = RoomType.objects.all()
    unique_halls = set()


    if(submitted):
        form = FilterForm(request.POST)
        if(form.is_valid()):
            # Get boolean value of checkbox
            # TODO: Assign here all the filter variables to
            # their respective values in the form
            search = submitted.get('search')


            #isCatered = form.cleaned_data.get('isCatered')

            catered = form.cleaned_data.get('eat_options')

            #isEnsuite = form.cleaned_data.get('isEnsuite')
            #hasBasin = form.cleaned_data.get('hasBasin')
            basin_ensuite = form.cleaned_data.get('toilet_options')

            print(basin_ensuite)

            #isSingle = form.cleaned_data.get('isSingle') #???
            #isDouble = form.cleaned_data.get('isDouble') #???

            bedsize = form.cleaned_data.get('bed_options')

            whichHall = form.cleaned_data.get('whichHall')
            min_price = submitted.get('price1')
            max_price = submitted.get('price2')
            Campus = submitted.get('Campus')

            # tries need to be seperate to allow only min price or only max price to be used
            try:
                min_price = int(min_price) * 100
            except:
                min_price = None # was 0 before?

            try:
                max_price = int(max_price) * 100
            except:
                max_price = None # was 0 before?


            # we use this to build up a query
            # query = [Q(ensuite=isEnsuite), Q(catered=isCatered), Q(basin=hasBasin), Q(bedsize__iexact=bedsize)]
            query = []
            
            #query.append(Q(catered=isCatered))
            
            #query.append(Q(bedsize__iexact=bedsize))

            if basin_ensuite == 'basin':
                query.append(Q(basin=True))
            elif basin_ensuite == 'ensuite':
                query.append(Q(ensuite=True))
            elif basin_ensuite == 'neither':
                query.append(Q(basin=False))
                query.append(Q(ensuite=False))
            

            if bedsize == 'single':
                query.append(Q(bedsize__iexact='Single'))
            elif bedsize == 'double':
                query.append(Q(bedsize__iexact='Double'))

            if catered == 'self':
                query.append(Q(catered=False))
            elif catered == 'catered':
                query.append(Q(catered=True))

            if min_price == None and max_price == None: # if both fields left empty
                #results_rooms = RoomType.objects.filter(ensuite=isEnsuite, catered=isCatered, basin=hasBasin, bedsize__iexact=bedsize)
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
                # TODO: need to add an error for
                #         - price1 > price2
                #         - if either are less than 0

            results_rooms = RoomType.objects.filter(*query)

            for i in results_rooms:
                unique_halls.add(i.hall)

                

    else:
        form = FilterForm()
        for i in results_rooms:
            unique_halls.add(i.hall)
        print(unique_halls)


    

    # Pass the halls data and the filters to the template form.html
    context = {
        'form': form,
        'results_rooms': results_rooms,
        'results_halls': unique_halls,
        'search': search,
        # 'isEnsuite': isEnsuite,
        # 'isCatered': isCatered,
        # 'hasBasin' : hasBasin,
        # 'isSingle' : isSingle,
        # 'isDouble': isDouble,
        # 'submitted': submitted,
        # 'price1': price1,
        # 'price2': price2,
        # 'Campus': Campus
    }
    return render(request, 'filter/form.html', context)
