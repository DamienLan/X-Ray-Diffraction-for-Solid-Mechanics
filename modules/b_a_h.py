# -*- coding: utf-8 -*-
"""
Program for the alignment of diffractometers with 1d detector:
    perform an OMEGA scan for a fixed detector position (while chi=0) and measure
    the Bragg peak displacement. Then estimate the horizontal beam misalignment
    to be corrected.
"""


import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from utils import display
from utils import maths_functions
from utils import seifert_data_TTX


# Horizontal beam position function
def beam_pos_h(data, *param):
    """
    Function providing displacement (dl) or peak position (ll) on the detector
    for a horizontal beam shift (e), during an omega scan
    units : angles in [deg], positions in [mm] or [pix]
    """
    e, l0 = param
    tth, ome = data
    deg2rad = np.pi / 180.
    dl = -e * np.sin((tth - ome) * deg2rad) / np.sin(ome * deg2rad)
    ll = l0 + dl
    return ll


def beam_align_h_analysis(dic):
    """
    Beam align h analysis using parameters stored in the dic
    """
    # Get the parameters from the dictionnary
    directory = dic["directory_beam_align_h"]
    filename = dic["filename_beam_align_h"]
    file_extension = dic["file_extension_beam_align_h"]
    display_before_removing = dic["display_before_removing_beam_align_h"]
    image_to_remove = dic["image_to_remove_beam_align_h"]
    display_after_removing = dic["display_after_removing_beam_align_h"]
    directory_clean = dic["directory_clean_beam_align_h"]
    filename_clean = dic["filename_clean_beam_align_h"]
    file_extension_clean = dic["file_extension_clean_beam_align_h"]
    save_clean_file = dic["save_clean_file_beam_align_h"]
    pixsize = dic["pixsize"]
    xmin = dic["window_xmin_beam_align_h"]
    xmax = dic["window_xmax_beam_align_h"]
    size_window_background_left = dic["size_window_background_left_beam_align_h"]
    size_window_background_right = dic["size_window_background_right_beam_align_h"]

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

    # Create new list without removed acquisition
    for ii in range(len(tth)):
        if not (ii + 1 in image_to_remove):
            tth_clean.append(tth[ii])
            omega_clean.append(omega[ii])
            chi_clean.append(chi[ii])
            phi_clean.append(phi[ii])
            cts_clean.append(cts[ii])

    # Save the clean file    
    if save_clean_file:
        seifert_data_TTX.write_seifert_data_TTX(tth_clean, omega_clean, chi_clean, phi_clean, cts_clean,
                                                directory_clean, filename_clean)
        print("Clean file saved.")

    # Display the acquisisiton after removing    
    if display_after_removing:
        display.display_image(directory_clean, filename_clean, file_extension_clean)

    # Read data from clean file
    tth, omega, chi, phi, cts = tth_clean, omega_clean, chi_clean, phi_clean, cts_clean

    # Acquisition parameters
    number_of_pixel = len(cts[0])
    number_of_image = len(tth)

    # Obtaining the median position, median intensity, median FWHM (H) and median A,B of the peak
    x0, IM, H, A, B = maths_functions.initial_guess(cts, xmin, xmax,
                                                    size_window_background_left, size_window_background_right)

    # Display the window of work
    x = np.arange(0, len(cts[0]), 1)
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_title(f'Work Window')
    ax.set_xlabel('Detector pixel [pix]')
    ax.set_ylabel('Intensity [cts]')
    for i in range(len(cts)):
        ax.plot(x[xmin:xmax], cts[i][xmin:xmax], label=f'image n°{i}')
    plt.show()

    # Display initial guess 
    print(f'Initial guess :\nx0 = {x0:4.3f}\nIM = {IM:4.3f}\nH = {H:4.3f}\nA = {A:4.3f}\nB = {B:4.3f}')

    # Reading, analizing and fiting

    # Fit the peak positions
    print('PEAK FIT')
    guess = [x0, IM, H, A, B]
    x = np.arange(0, number_of_pixel, 1)
    peakfit = []  # to store the peak fit results

    # fiting peaks for each image USING INITIAL GUESS FOR PEAK POSITION
    for ii in range(number_of_image):
        # popt : optimals parameters ; pcov : cova<riance matrice
        popt, pcov = curve_fit(maths_functions.gauss_backg, x[xmin:xmax], cts[ii][xmin:xmax], p0=guess)
        peakfit.append(popt)

    # central position of each peak
    peakpos = np.array([peakfit[ii][0] for ii in range(number_of_image)])

    # Peak position display
    print(f'(xx)    omega  pos[pix]')
    for ii in range(number_of_image):
        print(f'{ii + 1:3.0f}  {omega[ii]:8.3f} {peakpos[ii]:8.2f}')

    # Plot peak data and peak fit
    print()
    print('PEAK FIT => PLOT')
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_title(f'Omega scan for horizontal beam alignment')
    ax.set_xlabel('Detector pixel [pix]')
    ax.set_ylabel('Intensity [cts]')

    ax.set_xlim([xmin, xmax])

    for ii in range(number_of_image):
        ax.plot(x, cts[ii], '.', label=f'data {omega[ii]:5.2f}', markersize=6)
        ax.plot(x, maths_functions.gauss_backg(x, *peakfit[ii]), '-', label=f'fit  {omega[ii]:5.2f}')
    plt.legend()
    plt.show()

    # Estimate for the beam misalignment
    print('\nESTIMATE BEAM MISALIGNMENT')
    guess = [0, x0]  # initail guess for beam misalignment = 0 ; USING INITIAL GUESS FOR PEAK POSITION
    popt, pcov = curve_fit(beam_pos_h, (tth, omega), peakpos, p0=guess)

    # optimal paramaters
    e = popt[0]
    ch0 = popt[1]
    # standard deviation
    de = np.sqrt(pcov[0][0])
    dch0 = np.sqrt(pcov[1][1])

    # result display
    print(
        f'Horizontal beam misalignment : e  = {e:.2f} +- {de:.2f} pix / {e * pixsize:.3f} +- {de * pixsize:.2f} mm ({abs(de * 100 / e):3.1f} %)')
    print(f'Obtained peak position     : l0 = {ch0:.2f} +- {dch0:.2f} pix')

    # Plot beam_pos_h fit
    print('\nBEAM MISALIGNMENT => PLOT')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(f'2th = {tth[0]}, e = {e * pixsize:.3f} mm, peak_pos = {ch0:.2f} pix')
    ax.set_xlabel('Omega [deg]')
    ax.set_ylabel('Peak position [pix]')
    # data
    ax.plot(omega, peakpos, 'b.', label='data', markersize=6)
    # fit
    x = np.arange(np.min(omega) * 0.9, np.max(omega) * 1.1, 1.)
    tth = np.ones(len(x)) * tth[0]
    ax.plot(x, beam_pos_h((tth, x), *popt), '-r', label='fit', linewidth=0.5)

    plt.legend()
    plt.show()
