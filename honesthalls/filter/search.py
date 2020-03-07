from django.shortcuts import render
from django.db.models import Q
from .forms import *
from halls.models import Hall, RoomType, HallPhotos
from difflib import SequenceMatcher


def searching(search_string, unique_halls):
    '''Here is the matching.'''
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
        for j in range(i + 1, len(sorting_data)):
            if sorting_data[j][1] > sorting_data[i][1]:
                tem = sorting_data[i][0]
                sorting_data[i][0] = sorting_data[j][0]
                sorting_data[j][0] = tem
                tem = sorting_data[i][1]
                sorting_data[i][1] = sorting_data[j][1]
                sorting_data[j][1] = tem

    for c in range(count):
        results_rooms = RoomType.objects.filter(Q(hall__name__icontains=sorting_data[c][0]))
        for i in results_rooms:
            unique_halls.add(i.hall)
        for hall in unique_halls:
            hall.photos = list(HallPhotos.objects.filter(hall=hall))
    # TODO: Change so it only queries search results

    return results_rooms