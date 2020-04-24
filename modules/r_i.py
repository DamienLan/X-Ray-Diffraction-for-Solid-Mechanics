# -*- coding: utf-8 -*-
"""
Using a .CALI file and a .TTX file, get the image of one or some acquisition
"""


import numpy as np
import matplotlib.pyplot as plt

from utils import display
from utils import seifert_data_TTX
from utils import CALI_data


def read_image_analysis(dic):
    directory = dic["directory_read_image"]
    filename = dic["filename_read_image"]
    file_extension = dic["file_extension_read_image"]

    display_before_removing = dic["display_before_removing_read_image"]
    image_to_remove = dic["image_to_remove_read_image"]
    display_after_removing = dic["display_after_removing_read_image"]

    directory_clean = dic["directory_clean_read_image"]
    filename_clean = dic["filename_clean_read_image"]
    file_extension_clean = dic["file_extension_clean_read_image"]
    save_clean_file = dic["save_clean_file_read_image"]

    directory_CALI = dic["directory_CALI_read_image"]
    filename_CALI = dic["filename_CALI_read_image"]
    file_extension_CALI = dic["file_extension_CALI_read_image"]

    # Display the acquisisitons
    if display_before_removing:
        display.display_image(directory, filename, file_extension)

    # Read data of the scan
    tth, omega, chi, phi, cts = seifert_data_TTX.read_seifert_data_TTX(directory, filename, file_extension)

    # Remove acquisition (use display to check all the image) 
    tth_clean = []
    omega_clean = []
    chi_clean = []
    phi_clean = []
    cts_clean = []

    # create new liste without removed acquisition
    for ii in range(len(tth)):
        if not (ii + 1 in image_to_remove):
            tth_clean.append(tth[ii])
            omega_clean.append(omega[ii])
            chi_clean.append(chi[ii])
            phi_clean.append(phi[ii])
            cts_clean.append(cts[ii])

    # Save the file without removed acquisition
    if save_clean_file:
        seifert_data_TTX.write_seifert_data_TTX(tth_clean,
                                                omega_clean,
                                                chi_clean,
                                                phi_clean,
                                                cts_clean,
                                                directory_clean, filename_clean)
        print("Clean file saved.")

    # Getting all the data
    tth, omega, chi, phi, cts = tth_clean, omega_clean, chi_clean, phi_clean, cts_clean
    correction_pix = CALI_data.read_data_CALI(directory_CALI, filename_CALI, file_extension_CALI)

    # Display the acquisisiton after removing    
    if display_after_removing:
        display.display_image(directory_clean, filename_clean, file_extension_clean)

    # Using .CALI file and direct angle correction

    # Obtaining number of point (if .CALI file and .TTX file have not same dimension)
    number_of_point = min(len(cts[0]), len(correction_pix))
    number_of_image = len(tth)

    # Creation of cts real list : corrected intensity
    cts_real = []
    for ii in range(number_of_image):
        cts_real_acquisition = []
        for jj in range(number_of_point):
            cts_real_acquisition.append(cts[ii][jj] / np.cos(correction_pix[jj] * np.pi / 180))
        cts_real.append(cts_real_acquisition)

    # Creation of tth real list : corrected position
    tth_real = []
    for elem in tth:
        tth_real_acquisition = []
        for correction in correction_pix:
            tth_real_acquisition.append(elem + correction)
        tth_real.append(tth_real_acquisition)

    # getting parameters acquisition
    tth_min = min([min(elem) for elem in tth_real])
    tth_max = max([max(elem) for elem in tth_real])

    # Print acquisition parameters
    print('\nACQUISITION PARAMETERS :\n')
    print(f'Number of image = {number_of_image}')
    print(f'Number of pixel = {number_of_point}')
    print(f'2theta min = {tth_min:5.2f}')
    print(f'2theta max = {tth_max:5.2f}')

    # all the image with correction on the same diagram
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_title(f'{filename} : Complete diagram : {tth_min:5.2f}° - {tth_max:5.2f}° ')
    ax.set_xlabel('2theta [°]')
    ax.set_ylabel('Intensity [cts]')
    # ax.set_xlim(135,145)
    for ii in range(number_of_image):
        ax.plot(tth_real[ii], cts_real[ii][:number_of_point],
                label=f'Acquisiton n°{ii + 1} : {min(tth_real[ii]):5.2f}° - {max(tth_real[ii]):5.2f}°')

    plt.legend()
    plt.show()
