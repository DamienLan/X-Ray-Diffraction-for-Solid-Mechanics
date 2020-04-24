# -*- coding: utf-8 -*-
"""
Define function which display all the image of an acquisisition
"""


import numpy as np
import matplotlib.pyplot as plt

from utils import seifert_data_TTX


def display_image(directory, filename, extension='TTX'):
    """
    Display all the image of the acquisition
    """
    tth, omega, chi, phi, cts = seifert_data_TTX.read_seifert_data_TTX(directory, filename, extension)

    x = np.arange(0, len(cts[0]), 1)

    for i in range(len(cts)):
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.set_title(
            f'{filename}, image n°{i + 1} (tth_motor={tth[i]:4.1f}, omega={omega[i]:4.1f}, chi={chi[i]:4.1f}, phi={phi[i]:4.1f})')
        ax.set_xlabel('Detector pixel [pix]')
        ax.set_ylabel('Intensity [cts]')
        ax.plot(x, cts[i], label='data')
        plt.legend()
        plt.show()
