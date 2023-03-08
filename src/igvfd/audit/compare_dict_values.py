#!/usr/bin/env python
import sys


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


# generic value comparison function for possible dictionary or list values
def compare_unknown_type_values(
        key,
        value_one,
        value_two,
        ignore_key_set,
        differences):

    # determine how to compare the values
    if type(value_one) != type(value_two):
        # the values are not the same type
        # set up difference result
        differences.append(key)
        return False

    # check if is dictionary
    if isinstance(value_one, dict):
        # both must be dictionaries
        # recursive call
        return compare_dictionary_internal(
            value_one,
            value_two,
            ignore_key_set,
            differences)

    # check if is array
    if isinstance(value_one, list):
        # both must be arrays
        return compare_list_elements(
            key,
            value_one,
            value_two,
            ignore_key_set,
            differences)

    # try to compare values
    if value_one != value_two:
        # set up difference result
        differences.append(key)
        return False

    # successful comparison
    return True


# generic array comparison function
def compare_list_elements(
        key,
        list_one,
        list_two,
        ignore_key_set,
        differences):

    # check length of lists
    if len(list_one) != len(list_two):
        differences.append(key)
        return False

    # check if empty
    length_array = len(list_one)
    if length_array == 0:
        # nothing to compare in lists
        return True

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

        # compare unknown type values from list
        if not compare_unknown_type_values(
                key,
                value_one,
                value_two,
                ignore_key_set,
                differences):
            # return that a difference found
            return False

    # successful comparison
    return True


# generic dictionary comparison function
def compare_dictionary_internal(
        dict_one,
        dict_two,
        ignore_key_set,
        differences):

    # check if dictionaries
    if not isinstance(dict_one, dict):
        return False
    if not isinstance(dict_two, dict):
        return False

    # get keys from first dictionary
    comparison_keys = []
    for key in dict_one.keys():
        if key not in ignore_key_set:
            comparison_keys.append(key)

    # get keys from second dictionary
    for key in dict_two.keys():
        if (key not in comparison_keys) and (key not in ignore_key_set):
            comparison_keys.append(key)

    # return value
    is_successful = True

    # loop through keys
    for key in comparison_keys:
        # check if in first dictionary
        if key not in dict_one.keys():
            # set up difference result
            differences.append(key)
            # set that a difference found
            is_successful = False
            continue

        # check if in second dictionary
        if key not in dict_two.keys():
            # set up difference result
            differences.append(key)
            # set that a difference found
            is_successful = False
            continue

        # the value has to be in both dictionaries
        value_one = dict_one[key]
        value_two = dict_two[key]

        # compare dictionary values
        if not compare_unknown_type_values(
                key,
                value_one,
                value_two,
                ignore_key_set,
                differences):
            # set that a difference found
            is_successful = False

    # return if comparison successful to avoid duplicate keys for list comparison
    return is_successful
