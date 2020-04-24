# -*- coding: utf-8 -*-
"""
Define mathematical functions
"""


import numpy as np
from numpy.polynomial import Polynomial

from utils import list_manipulation


def gauss(x, *p):
    """
    Gaussian distribution (3 parameters)
    * x0 : central position
    * IM : intensity max
    * H  : FWHM
    """
    x0, IM, H = p
    # 2.77258872224 = 4*ln(2)
    y = IM * np.exp(-2.77258872224 * (x - x0) ** 2 / H ** 2)
    return y


# polynomial function for background
def polynomial(x, *p):
    """
    Polynomial function: y = p[0] + p[1]*x + p[2]*x^2 + p[3]*x^3 + ...
    """
    poly = Polynomial(p)
    y = poly(x)
    return y


# real peak function (gaussian + background)
def gauss_backg(x, *p):
    """
    Gaussian distribution with linear background (5 parameters)
    * x0 : central position
    * IM : intensity max
    * H  : FWHM
    * background y = A + Bx
    """
    y = gauss(x, *p[0:3]) + polynomial(x, *p[3:5])
    return y


def trapeze_method(listy, step):
    """
    Calcul the integral of the function corresponding at the liste using the trapeze method
    """

    add = 0

    for ii in range(len(listy) - 1):
        add += 0.5 * step * (listy[ii + 1] + listy[ii])

    return add


def initial_guess(cts, xmin, xmax, size_window_background_left, size_window_background_right):
    """
    Calcul x0, IM, H, A and B median using for initial guess for the peak fit
    """

    # Automatic finding peak parameters
    number_of_image = len(cts)  # nbre of images in the scan

    add_x0 = 0
    add_IM = 0
    add_H = 0
    add_A = 0
    add_B = 0

    for ii in range(number_of_image):
        number_of_pixel = len(cts[ii])
        x = np.arange(0, number_of_pixel, 1)
        step = x[1] - x[0]

        # Obtaining and add x0, IM and H
        add_x0 += (xmin + list_manipulation.index(cts[ii][xmin:xmax], max(cts[ii][xmin:xmax])))
        add_IM += max(cts[ii][xmin:xmax])
        add_H += (trapeze_method(cts[ii][xmin:xmax], step) / max(cts[ii][xmin:xmax]))

        # Obtaining A and B
        background_left = cts[ii][xmin:xmin + size_window_background_left]
        background_right = cts[ii][xmax - size_window_background_right:xmax]

        left_point_value = np.mean(background_left)
        right_point_value = np.mean(background_right)

        left_point_absc = xmin + size_window_background_left / 2
        right_point_absc = xmax - size_window_background_right / 2

        B_temp = (left_point_value - right_point_value) / (left_point_absc - right_point_absc)
        A_temp = left_point_value - B_temp * left_point_absc

        add_A += A_temp
        add_B += B_temp

    x0 = add_x0 / number_of_image
    IM = add_IM / number_of_image
    H = add_H / number_of_image
    A = add_A / number_of_image
    B = add_B / number_of_image

    return x0, IM, H, A, B