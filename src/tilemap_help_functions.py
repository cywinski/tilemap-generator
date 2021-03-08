import numpy as np
from random import randint


def convert_to_np(ls, dtype=None):
    """
    Function that converts list to NumPy array with provided data type

    :param ls: List to convert
    :type ls: list
    :param dtype: Data type of NumPy array
    """

    return np.array(ls) if not dtype else np.array(ls, dtype=dtype)


def find_every_zero(np_array):
    """
    Function that finds coordinates of zeros' occurrences

    :param np_array: NumPy array where User wants to find zeros
    :type np_array: numpy.ndarray
    """

    return np.where(np_array == 0)


def stack_array(array1, array2):
    """
    Function that stacks two arrays in one

    :param array1: First provided array to stack
    :type array1: numpy.ndarray
    :param array2: Second provided array to stack
    :type array2: numpy.ndarray
    """

    return np.vstack((array1, array2))


def choose_random_coordinate(limit1, limit2):
    """
    Function that chooses two random values within provided range

    :param limit1: First high limit
    :type limit1: int
    :param limit2: Second high limit
    :type limit2: int
    """

    modified_x = randint(0, limit1 - 1)
    modified_y = randint(0, limit2 - 1)
    return modified_x, modified_y


def add_to_set(used_set, item):
    """
    Function that adds provided item to set

    :param used_set: Provided set of items
    :type used_set: set
    :param item: Provided item
    """

    used_set.add(item)
