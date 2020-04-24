# -*- coding: utf-8 -*-
"""
Program for the alignment of diffractometers with 1d detector:
    perform an CHI scan for a fixed detector position (while omega=cst) and measure
    the Bragg peak displacement. Then estimate the vertical beam misalignment
    to be corrected.
"""


import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from utils import display
from utils import maths_functions
from utils import seifert_data_TTX


# Vertical beam position function
def beam_pos_v(data, *param):
    """
    Function providing displacement (dl) or peak position (ll) on the detector
    for a vertical beam shift (h), during a chi scan
    units : angles in [deg], positions in [mm] or [pix]
    """
    h, l0 = param
    tth, ome, psi = data
    deg2rad = np.pi / 180.
    dl = h * np.tan(psi * deg2rad) * np.sin(tth * deg2rad) / np.sin(ome * deg2rad)
    ll = l0 + dl
    return ll


def beam_align_v_analysis(dic):
    """
    Beam align v analysis using parameters stored in the dic
    """
    # Get the parameters from the dictionnary
    directory = dic["directory_beam_align_v"]
    filename = dic["filename_beam_align_v"]
    file_extension = dic["file_extension_beam_align_v"]
    display_before_removing = dic["display_before_removing_beam_align_v"]
    image_to_remove = dic["image_to_remove_beam_align_v"]
    display_after_removing = dic["display_after_removing_beam_align_v"]
    directory_clean = dic["directory_clean_beam_align_v"]
    filename_clean = dic["filename_clean_beam_align_v"]
    file_extension_clean = dic["file_extension_clean_beam_align_v"]
    save_clean_file = dic["save_clean_file_beam_align_v"]
    pixsize = dic["pixsize"]
    xmin = dic["window_xmin_beam_align_v"]
    xmax = dic["window_xmax_beam_align_v"]
    size_window_background_left = dic["size_window_background_left_beam_align_v"]
    size_window_background_right = dic["size_window_background_right_beam_align_v"]

    # Display the acquisiton
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
    print()
    print('PEAK FIT')
    guess = [x0, IM, H, A, B]
    x = np.arange(0, number_of_pixel, 1)
    peakfit = []  # to store the peak fit results
    for ii in range(number_of_image):
        popt, pcov = curve_fit(maths_functions.gauss_backg, x[xmin:xmax], cts[ii][xmin:xmax], p0=guess)
        peakfit.append(popt)

    # Get central position for each peak
    peakpos = np.array([peakfit[ii][0] for ii in range(number_of_image)])

    print(f'(xx)    chi     pos[pix]')
    for ii in range(number_of_image):
        print(f'{ii + 1:3.0f}  {chi[ii]:8.3f} {peakpos[ii]:8.2f}')

    # Plot peak data and peak fit
    print()
    print('PEAK FIT => PLOT')
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_title(f'Chi scan for horizontal beam alignment : {filename}')
    ax.set_xlabel('Detector pixel [pix]')
    ax.set_ylabel('Intensity [cts]')

    ax.set_xlim([xmin, xmax])

    for ii in range(number_of_image):
        ax.plot(x, cts[ii], '.', label=f'data {chi[ii]:5.2f}', markersize=6)
        ax.plot(x, maths_functions.gauss_backg(x, *peakfit[ii]), '-', label=f'fit  {chi[ii]:5.2f}')

    plt.legend()
    plt.show()

    # Estimate for the beam misalignment
    print()
    print('ESTIMATE BEAM MISALIGNMENT')
    guess = [0, x0]
    popt, pcov = curve_fit(beam_pos_v, (tth, omega, chi), peakpos, p0=guess)

    # Optimal parmaters
    h = popt[0]
    ch0 = popt[1]
    # Standard deviation
    dh = np.sqrt(pcov[0][0])
    dch0 = np.sqrt(pcov[1][1])

    # result display
    print(
        f'Vertical beam misalignment : h  = {h:.2f} +- {dh:.2f} pix / {h * pixsize:.3f} +- {dh * pixsize:.2f} mm ({abs(dh * 100 / h):3.1f} %)')
    print(f'Obtained peak position     : l0 = {ch0:.2f} +- {dch0:.2f} pix')

    # Plot beam_pos_v fit
    print('\nBEAM MISALIGNMENT => PLOT')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(f'2th = {tth[0]}, h = {h * pixsize:.3f} mm, peak_pos = {ch0:.2f} pix')
    ax.set_xlabel('Chi [deg]')
    ax.set_ylabel('Peak position [pix]')
    # Data
    ax.plot(chi, peakpos, 'b.', label='data', markersize=6)
    # Fit
    length = np.max(np.abs(chi)) * 1.1
    chi = np.arange(-length, length, 1.)
    ome = np.ones(len(chi)) * omega[0]
    tth = np.ones(len(chi)) * tth[0]
    ax.plot(chi, beam_pos_v((tth, ome, chi), *popt), '-r', label='fit', linewidth=0.5)

    plt.legend()
    plt.show()
