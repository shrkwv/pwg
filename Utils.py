#!/usr/bin/env python
from __future__ import unicode_literals

import re
import itertools
from string import maketrans
from Token import Token


# def part_to_min_max(part):
#     """ convert part to min max
#     :param part: a:b
#     :return:min_size, max_size
#     """
# # regex for parts
#     max_size_regex = re.compile("^\:[\-?\d]+$")
#     min_size_regex = re.compile("^[\-?\d]+\:$")
#     min_and_max_regex = re.compile("^[\-?\d]+[\:][\-?\d]+$")
#     specific_size_regex = re.compile("^\d+$")
#
#     min_size = None
#     max_size = None
#
#     if re.match(max_size_regex,part):
#         max_size = int(part[1:])
#
#     elif re.match(min_size_regex,part):
#         min_size = int(part[:-1])
#
#     elif re.match(min_and_max_regex,part):
#         splited_part = part.split(':')
#         min_size = int(splited_part[0])
#         max_size = int(splited_part[1])
#
#     elif re.match(specific_size_regex, part):
#         min_size = int(part)
#         max_size = int(part)
#
#     return min_size, max_size


def part_to_min_max(part):

    """
    return min max tuple for range input parameter
    """
    delimiters = re.compile("[\:|\,|\s]")
    part = str(part)
    result = re.split(delimiters, part)
    if len(result) == 1:
        result.append(result[0])

    min_size, max_size = result
    if min_size:
        min_size = int(min_size)
    else:
        min_size = None
    if max_size:
        max_size = int(max_size)
    else:
        max_size = None
    return min_size, max_size


def get_partial_values(list_of_strings, python_part_as_string):
    """
    get list of string and charses in the python way ([a:b])
    """
    min_size, max_size = part_to_min_max(python_part_as_string)

    values = list_of_strings

    result = []
    for value in values:
        if min_size == max_size and not min_size is None:

            new_value = value[min_size]
        elif min_size == None or min_size==0:
            new_value = value[:max_size]
        elif max_size == None:
            new_value = value[min_size:]
        elif max_size and min_size:
            new_value = value[min_size:max_size]
        else:
            pass
        if new_value:
            result.append(new_value)

    return result


def scramble_upper_lower_conversion(word):
    """scrambling upper and lower case
    :return list of all possible scramble
    """
    scramble_list = map(''.join, itertools.product(*zip(word.upper(), word.lower())))

    return scramble_list


def basic_leet_conversion(word):
    """
    return all possible leet for
    """
    # TODO leet for all possibilites
    english = 'aeiolAEIOL'
    basic_leet = '4310143101'
    translate_table = maketrans(english, basic_leet)
    word = str(word)
    full_leet_word = word.translate(translate_table)
    all_leet_options = map(''.join, itertools.product(*zip(word, full_leet_word)))
    result = list(set(all_leet_options))
    # result = result.remove(word)
    # leet_list.append(full_leet_word)
    return sorted(result)


def manipulate_list(function,wordlist):
    """
    manipulate function on given list of strings.
    """
    result = []

    if function == "upper":
        result = [item.upper() for item in wordlist]
    elif function == "lower":
        result = [item.lower() for item in wordlist]
    elif function == "capitalize":
        result = [item.capitalize() for item in wordlist]
    elif function == "title":
        result = [item.title() for item in wordlist]
    elif function == "scramble":
        # for english only.
        for word in wordlist:
            cur_scramble_list = scramble_upper_lower_conversion(word)
            result += cur_scramble_list
    elif function == "strip":
        delimiters = re.compile("[^A-Za-z0-9]")
        # result = [item.replace(" ","") for item in wordlist]
        result = [''.join(re.split(delimiters,item)) for item in wordlist]

    elif function == "splitall":
        delimiters = re.compile("[^A-Za-z0-9]")
        tmp_result = [re.split(delimiters, item) for item in wordlist]

        for tup in tmp_result:
            [result.append(t) for t in tup]

    elif function == "leet":
        for word in wordlist:
            leet_list = basic_leet_conversion(word)
            result += leet_list
    # all dates possibilities
    elif function == "dates":
        result = f_dates(wordlist)
    elif function == "reverse":
        result = [item[::-1] for item in wordlist]

    elif function == "initials":
        for word in wordlist:
            splitted_word = word.split()
            initials = [items[0] for items in splitted_word]
            result.append(''.join(initials))

    return result



def f_dates(list_of_dates):

    delimiters = re.compile("[^A-Za-z0-9]")
    dates = [re.split(delimiters, item) for item in list_of_dates]
    result = []
    for date in dates:
        d_y = True
        result_for_date = []
        two_chars_year = date[2][-2:]

        years = (two_chars_year, date[2])
        result_for_date += [item for item in years]
        months = (date[1],)
        days = (date[0],)

        if months[0].startswith("0"):
            months = (months[0], months[0][1])
        else:
            d_y = False
        if days[0].startswith("0"):
            days = (days[0], days[0][1])
        else:
            d_y = False
        result_for_date += [item for item in days]
        result_for_date += [item for item in months]
        # ddmm
        result_for_date.append(days[0] + months[0])
        #mmdd
        result_for_date.append(months[0]+days[0])
        #ddmmyy
        result_for_date.append(days[0] + months[0]+years[1])
        #ddmmyyyy
        result_for_date.append(days[0] + months[0]+years[0])
        #mmddyyyy
        result_for_date.append(months[0]+days[0]+years[0])
        #yyyyddmm
        result_for_date.append(years[0] + days[0] + months[0])
        #yyddmm
        result_for_date.append(years[1] + days[0]+months[0])

        if d_y:

            #dmyyyy
            result_for_date.append(days[1] + months[1] + years[0])
            #dmyy
            result_for_date.append(days[1] + months[1] + years[1])
            #dm
            result_for_date.append(days[1]+ months[1])
        result += list(set(result_for_date))

    return list(set(result))

# special functions

def special_manipulate_list(function, wordlist, args):
        """

        :param function:
        :param wordlist:
        :param args:
        :return: results
        """
        result = []
        if function == "add":
            string = args[0][1:-1]
            index = int(args[1])
            result = s_add(wordlist, string, index)

        elif function == "replace":
            old_string = args[0][1:-1]
            new_string = args[1][1:-1]
            result = s_replace(wordlist, old_string, new_string)

        elif function == "split":
            delimiter = str(args[0][1:-1])
            if len(args) == 2:
                part = args[1]
                min_split, max_split = part_to_min_max(part)
                delimiter = str(delimiter)
                result = s_split(wordlist, delimiter, min_split, max_split)
            else:
                result = s_split(wordlist, delimiter)
        elif function == "multiply":
            part = args[0]
            min_split, max_split = part_to_min_max(part)

            result = s_multiply_strings(wordlist, min_split, max_split)
        return result

# TODO s_merge
def s_add(list_of_words, string, index):
    """ add string to list of words in the index specified
    :param token:
    :param string:
    :param index:
    :return:manipulated_list
    """
    manipulated_list = []
    for word in list_of_words:
        word = word[:index] + string + word[index:]
        manipulated_list.append(word)

    return manipulated_list


def s_replace(list_of_words, old, new):

    manipulated_list = []
    for word in list_of_words:
        word = str(word)
        word = word.replace(old, new)
        manipulated_list.append(word)

    return manipulated_list


def s_split(list_of_words, delimiter, from_word, to_word):
    """

    :param list_of_words:
    :param delimiter:
    :param min_split:
    :param max_split:
    :return:
    """

    manipulated_list = []
    for word in list_of_words:
        word = str(word)
        splitted_word = word.split(delimiter)

        if splitted_word[0] == word:
            continue
        if from_word == to_word:
            result_word = splitted_word[from_word]
        else:
            result_word = delimiter.join(splitted_word[from_word:to_word])

        if result_word:
            manipulated_list.append(result_word)
        else:
            continue

    return manipulated_list

def s_multiply_strings(list_of_words, multiply_min,multiply_max):
    """

    :param list_of_words:
    :param multiply_in:
    :param all:
    :return:
    """
    result = []
    if multiply_min == multiply_max and multiply_max is not None and multiply_min is not None:
        result += map(''.join, itertools.permutations(list_of_words, multiply_max))
        return result
    if multiply_max is None:
        # TODO exception
        multiply_max = multiply_min+1
    if multiply_min is None:
        multiply_min = 0



    for i in range(multiply_min,multiply_max+1):
        # result = map(''.join, itertools.product(list_of_words, repeat=multiply_in))

        result += map(''.join, itertools.permutations(list_of_words, i))

    return result

# def s_dates(list_of_dates, number_of_elements):
#     # TODO dates function
#     delimiters = re.compile("[^A-Za-z0-9]")
#     dates = [re.split(delimiters, item) for item in list_of_dates]
#     result = []
#     for date in dates:
#         two_chars_year = date[2][-2:]
#
#         years = (two_chars_year, date[2])
#         result += [item for item in years]
#         months = (date[1],)
#         days = (date[0],)
#
#         if months[0].startswith("0"):
#             months = (months[0], months[0][1])
#         if days[0].startswith("0"):
#             days = (days[0], days[0][1])
#         result += [item for item in days]
#         result += [item for item in months]
#
#
#
#         all_dates = days+months+years
#         # permutations_2_date = list(itertools.permutations(all_dates,r=2))
#         # print permutations_2_date
#         two_elements = list(itertools.permutations(all_dates, 2))
#         three_elements = list(itertools.permutations(all_dates, 3))


def s_merge(list_1, list_2):
    pass
#special counters

def count_scramble_options(word):
    """return the number of possible options
    """
    value_alpha_chars = re.findall(r'[a-zA-Z]', word)
    number_of_options = 2**len(value_alpha_chars)

    return number_of_options

def valid_size(word, min_length=None, max_length=None):
    """
    create the equal regex for the input sizes by the user
    """
    word_length = len(word)
    result = True
    if min_length:
        if word_length < min_length:
            result = False
    if max_length:
        if word_length > max_length:
            result = False

    return result

