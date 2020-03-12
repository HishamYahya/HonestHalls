import json
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

from halls.models import Hall

def map(request):
    halls = Hall.objects.all()
    hall_data = [hall.get_card_data() for hall in halls]
    for hall in hall_data:
        # Get the actual Django instance
        hall_instance = halls.get(pk=hall.get('id'))
        # And query all the rooms, taking only the formatted_string to pass to the view
        hall['room_descs'] = [roomtype.formatted_string for roomtype in hall_instance.roomtype_set.all()]

    hall_data_json = json.dumps(list(hall_data), cls=DjangoJSONEncoder)
    return render(request, 'maps/map.html', {
        'halls': hall_data,
        'hall_data_json': hall_data_json
    })
