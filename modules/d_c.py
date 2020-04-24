# -*- coding: utf-8 -*-
"""
Program for the calibration for 1D-detector:
    preform a 2theta scan WITHOUT sample : direct incidence
    scan : 2theta around -12° ==> 2theta around +12°
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

from utils import display
from utils import seifert_data_TTX
from utils import CALI_data
from utils import fit_one_peak


def detector_calibration_analysis(dic):
    directory = dic["directory_detector_calibration"]
    filename = dic["filename_detector_calibration"]
    file_extension = dic["file_extension_detector_calibration"]

    display_before_removing = dic["display_before_removing_detector_calibration"]
    image_to_remove = dic["image_to_remove_detector_calibration"]
    display_after_removing = dic["display_after_removing_detector_calibration"]

    directory_clean = dic["directory_clean_detector_calibration"]
    filename_clean = dic["filename_clean_detector_calibration"]
    file_extension_clean = dic["file_extension_clean_detector_calibration"]
    save_clean_file = dic["save_clean_file_detector_calibration"]

    directory_CALI = dic["directory_CALI_detector_calibration"]
    filename_CALI = dic["filename_CALI_detector_calibration"]
    file_extension_CALI = dic["file_extension_CALI_detector_calibration"]
    save_CALI = dic["save_CALI_detector_calibration"]


    # Display the acquisisiton
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

    # Save the clean file
    if save_clean_file:
        seifert_data_TTX.write_seifert_data_TTX(tth_clean, omega_clean, chi_clean, phi_clean, cts_clean, directory_clean, filename_clean)
        print("Clean file saved.")

    # Display the acquisisiton after removing
    if display_after_removing:
        display.display_image(directory_clean, filename_clean, file_extension_clean)

    # Read data from clean data
    tth, omega, chi, phi, cts = tth_clean, omega_clean, chi_clean, phi_clean, cts_clean

    # Fitting all the peak
    # list with all the central position
    peakpos = []

    for image in cts:
        peakpos.append(fit_one_peak.fit_one_peak(image)[0][0])

    # fitting peakpos in function of tth : for each pixel you obtain the direct correction to add
    number_of_pixel = len(cts[0])
    pix = np.arange(1, number_of_pixel + 1, 1)

    # Fit
    fit_tth_peak_pos = interpolate.interp1d(peakpos, tth, fill_value="extrapolate", kind="linear")

    # tth angle for each pixel
    fit_tth_peak_pos_pix = []
    for pixel in pix:
        fit_tth_peak_pos_pix.append(fit_tth_peak_pos(pixel))

    # Correction for each pixel
    correction_pix = [-elem for elem in fit_tth_peak_pos_pix]

    # Plot
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_title(f'Direct angle correction')
    ax.set_xlabel('pixel')
    ax.set_ylabel('2theta motor')
    # ax.set_xlim(100,200)
    ax.plot(peakpos, tth, '.', label='data')
    ax.plot(pix, correction_pix, label='correction')
    ax.plot(pix, fit_tth_peak_pos_pix, '--', label='fit')
    plt.legend()
    plt.show()

    # Save .CALI file : direct angle correction    
    # Write .CALI file

    if save_CALI:
        CALI_data.write_data_CALI(correction_pix, directory_CALI, filename_CALI, file_extension_CALI)
        print('.CALI file saved')
