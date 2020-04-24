# -*- coding: utf-8 -*-
"""
Define list manipulation function
"""


def index(liste, value):
    """
    return the index corresponding at the first occurence of value in list
    """

    for ii in range(len(liste)):
        if liste[ii] == value:
            return ii
    return None
