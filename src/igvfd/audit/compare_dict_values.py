#!/usr/bin/env python
import sys
from dataclasses import dataclass


# class for output dictionary comparison
@dataclass
class DictDifference:
    item_key: str
    item_1_value: any
    item_2_value: any
    message: str


# generic dictionary comparison function
def compare_dictionary(
        dict_one,
        dict_two,
        ignore_keys):

    # set up list to return
    differences = []

    # create set for ignore keys so comparison is fast
    ignore_key_set = set()
    for key in ignore_keys:
        ignore_key_set.add(key)

    # call to compare dictionaries
    compare_dictionary_internal(
        dict_one,
        dict_two,
        ignore_key_set,
        differences)

    # return result
    return differences


# generic array comparison function
def compare_list_elements(
        key,
        list_one,
        list_two,
        ignore_key_set,
        differences):

    # check length of lists
    if len(list_one) != len(list_two):
        found_difference = DictDifference(key, list_one, list_two, 'lists are different lengths')
        differences.append(found_difference)
        return

    # check if empty
    length_array = len(list_one)
    if length_array == 0:
        return

    # use copy to not affect original arrays
    list_one_sorted = list_one.copy()
    list_two_sorted = list_two.copy()

    # sort the lists for comparison
    list_one_sorted.sort()
    list_two_sorted.sort()

    # loop through the elements of the array
    for index in range(length_array):

        # get values
        value_one = list_one_sorted[index]
        value_two = list_two_sorted[index]

        # determine how to compare the values
        if type(value_one) != type(value_two):
            # the values are not the same type
            # set up difference result
            found_difference = DictDifference(key, list_one, list_two, 'list values are different types')
            differences.append(found_difference)
            continue

        # check if is dictionary
        if isinstance(value_one, dict):
            # both must be dictionaries
            # recursive call
            compare_dictionary_internal(
                value_one,
                value_two,
                ignore_key_set,
                differences)
            continue

        # check if is array
        if isinstance(value_one, list):
            # both must be arrays
            compare_list_elements(
                key,
                value_one,
                value_two,
                ignore_key_set,
                differences)
            continue

        # try to compare values
        if value_one != value_two:
            # set up difference result
            found_difference = DictDifference(key, list_one, list_two, 'list values are different')
            differences.append(found_difference)
            break


# generic dictionary comparison function
def compare_dictionary_internal(
        dict_one,
        dict_two,
        ignore_key_set,
        differences):

    # check if dictionaries
    if not isinstance(dict_one, dict):
        return
    if not isinstance(dict_two, dict):
        return

    # get keys from first dictionary
    comparison_keys = []
    for key in dict_one.keys():
        if key not in ignore_key_set:
            comparison_keys.append(key)

    # get keys from second dictionary
    for key in dict_two.keys():
        if (key not in comparison_keys) and (key not in ignore_key_set):
            comparison_keys.append(key)

    # loop through keys
    for key in comparison_keys:
        # check if in first dictionary
        if key not in dict_one.keys():
            # get value from second dictionary
            # the value is not in first dictionary, so has to be in the second
            value = dict_two[key]
            # set up difference result
            found_difference = DictDifference(key, None, value, 'key not in first')
            differences.append(found_difference)
            continue

        # check if in second dictionary
        if key not in dict_two.keys():
            # get value from first dictionary
            # the value is not in second dictionary, so has to be in the first
            value = dict_one[key]
            # set up difference result
            found_difference = DictDifference(key, value, None, 'key not in second')
            differences.append(found_difference)
            continue

        # the value has to be in both dictionaries
        value_one = dict_one[key]
        value_two = dict_two[key]

        # determine how to compare the values
        if type(value_one) != type(value_two):
            # the values are not the same type
            # set up difference result
            found_difference = DictDifference(key, value_one, value_two, 'values are different types')
            differences.append(found_difference)
            continue

        # check if is dictionary
        if isinstance(value_one, dict):
            # both must be dictionaries
            # recursive call
            compare_dictionary_internal(
                value_one,
                value_two,
                ignore_key_set,
                differences)
            continue

        # check if is array
        if isinstance(value_one, list):
            # both must be arrays
            compare_list_elements(
                key,
                value_one,
                value_two,
                ignore_key_set,
                differences)
            continue

        # try to compare values
        if value_one != value_two:
            # set up difference result
            found_difference = DictDifference(key, value_one, value_two, 'values are different')
            differences.append(found_difference)
