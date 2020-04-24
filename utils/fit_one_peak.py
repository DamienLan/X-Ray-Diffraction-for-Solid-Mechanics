# -*- coding: utf-8 -*-
"""
Define fit one peak function use by detector calibration module
"""


import numpy as np
from scipy.optimize import curve_fit

from utils import list_manipulation
from utils import maths_functions


def fit_one_peak(image):
    """
    Take in argument a list corresponding at an image with only one peak
    return optimal parameters for a gaussian_background function of this peak
    """

    # Obtaining initial guess

    # choose the size of the window on wich the background is calculated
    size_window_background = 20

    x = np.arange(0, len(image), 1)
    step = x[1] - x[0]

    # central position
    x0 = list_manipulation.index(image, max(image)) + 1  # pixel beginning at zero
    # maximale intensity
    IM = max(image)
    # FWHM ~= Area/IM
    H = maths_functions.trapeze_method(image, step) / IM

    # getting a and B coefficient for the background
    background_left = image[0:size_window_background]
    background_right = image[len(image) - size_window_background:len(image)]

    left_point_value = np.mean(background_left)
    right_point_value = np.mean(background_right)

    left_point_absc = size_window_background / 2
    right_point_absc = len(image) - size_window_background / 2

    B = (left_point_value - right_point_value) / (left_point_absc - right_point_absc)
    A = left_point_value - B * left_point_absc

    # initial guess
    guess = [x0, IM, H, A, B]

    # Fiting and getting optimals parameters
    x = np.arange(1, len(image) + 1, 1)  # pixels beginning at 1
    popt, pcov = curve_fit(maths_functions.gauss_backg, x, image, p0=guess)

    # return optimal parameters
    return popt, pcov

