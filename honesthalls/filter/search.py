from django.shortcuts import render
from django.db.models import Q
from .forms import *
from halls.models import Hall, RoomType, HallPhotos
from difflib import SequenceMatcher


def searching(search_string):
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
                    result_matcher[count].append(hall.id)
                    result_matcher[count].append(1)
                    result_matcher[count].append(0)
                    result_matcher[count].append(0)
                    for j in range(i):
                        result_matcher[count][1] *= matcher[j][0]
                        result_matcher[count][2] = max(result_matcher[count][2], matcher[j][1])
                        result_matcher[count][3] = max(result_matcher[count][3], matcher[j][2])
                result_matcher[count][1] *= matcher[num][0]
                result_matcher[count][2] = max(result_matcher[count][2], matcher[num][1])
                result_matcher[count][3] = max(result_matcher[count][3], matcher[num][2])
            num += 1
        print(result_matcher)
        if record:
            count += 1

    """from here is the sorting"""
    id_list = []
    sorting_data = []
    for i in range(len(result_matcher)):
        id_list.append(result_matcher[i][0])
        sorting_data.append(max(result_matcher[i][1] * 2, result_matcher[i][2], result_matcher[i][3]))

    for i in range(len(sorting_data)):
        for j in range(i + 1, len(sorting_data)):
            if sorting_data[j] > sorting_data[i]:
                tem = id_list[i]
                id_list[i] = id_list[j]
                id_list[j] = tem
                tem = sorting_data[i]
                sorting_data[i] = sorting_data[j]
                sorting_data[j] = tem

    results_rooms = RoomType.objects.filter(Q(hall__id__in=[i for i in id_list]))

    # TODO: Change so it only queries search results
    # Make sure result_rooms is valid
    # even if there is no data match to the search_string

    if results_rooms == []:
        results_rooms = RoomType.objects.filter(Q(hall__name__iexact=search_string))

    return results_rooms