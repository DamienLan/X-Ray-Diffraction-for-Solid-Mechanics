# -*- coding: utf-8 -*-
"""
X-Ray Diffraction for Solid Mechanics

Author: Olivier Castelnau (olivier.castelnau@ensam.eu), lab PIMM (CNRS UMR8006) at ENSAM Paris, France.
        Vincent MICHEL (vincent.michel@ensam.eu)
        Damien LANASPEZE (damien.lanaspeze@mines-paristech.fr)

Program for the alignment of diffractometers with 1d detector:
    perform an OMEGA scan for a fixed detector position (while chi=0) and measure
    the Bragg peak displacement. Then estimate the horizontal beam misalignment
    to be corrected.
"""


import time

from modules import b_a_h
from utils import parameters_files


# Common parameters
pixsize = 0.14  # mm
R = 295  # mm

# Analysis parameters

# .TTX file informations
directory = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\experiments\omega_scan'
filename = 'omega_scan 21-11'
file_extension = '.TTX'

# Display before removing : True or False
display_before_removing = False
# Put here the number of the image(s) to remove
image_to_remove = []
# Display before removing : True or False
display_after_removing = False

# Save clean file : True or False
save_clean_file = False
# .TTX clean file informations
directory_clean = directory
filename_clean = filename + '_clean'
file_extension_clean = file_extension

# Windows position [pix] for peak fit : you have to see all the pic and around 30 pixel of background on each side
xmin = 120
xmax = 200

# Size of the background window for each side of the peak
size_window_background_left = 10
size_window_background_right = 10

# Saving Parameters on .PARAM file
save_PARAMfile_beam_align_h = False
# . PARAM file informations
directory_PARAM_beam_align_h = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\parameters'
filename_PARAM_beam_align_h = time.strftime("%d_%B_%Y") + '_beam_align_h'
file_extension_PARAM_beam_align_h = '.PARAM'

# Uploading parameters from a .PARAM file (!! the parameters use by the pragram will not be the previous parameters !!)
upload_PARAM_file = True
directory_upload_PARAM_beam_align_h = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\parameters'
filename_upload_PARAM_beam_align_h = '17_April_2020' + '_beam_align_h'
file_extension_upload_PARAM = '.PARAM'

# Parameters dictionnary
parameters_beam_align_h = dict()
parameters_beam_align_h["pixsize"] = pixsize
parameters_beam_align_h["goniometric_ray"] = R
parameters_beam_align_h["directory_beam_align_h"] = directory
parameters_beam_align_h["filename_beam_align_h"] = filename
parameters_beam_align_h["file_extension_beam_align_h"] = file_extension
parameters_beam_align_h["display_before_removing_beam_align_h"] = display_before_removing
parameters_beam_align_h["image_to_remove_beam_align_h"] = image_to_remove
parameters_beam_align_h["display_after_removing_beam_align_h"] = display_after_removing
parameters_beam_align_h["directory_clean_beam_align_h"] = directory_clean
parameters_beam_align_h["filename_clean_beam_align_h"] = filename_clean
parameters_beam_align_h["file_extension_clean_beam_align_h"] = file_extension_clean
parameters_beam_align_h["save_clean_file_beam_align_h"] = save_clean_file
parameters_beam_align_h["window_xmin_beam_align_h"] = xmin
parameters_beam_align_h["window_xmax_beam_align_h"] = xmax
parameters_beam_align_h["size_window_background_left_beam_align_h"] = size_window_background_left
parameters_beam_align_h["size_window_background_right_beam_align_h"] = size_window_background_right

if __name__ == '__main__':

    if save_PARAMfile_beam_align_h:
        parameters_files.save_param_file(parameters_beam_align_h,
                                         directory_PARAM_beam_align_h,
                                         filename_PARAM_beam_align_h,
                                         file_extension_PARAM_beam_align_h)

    if upload_PARAM_file:
        parameters_beam_align_h = parameters_files.upload_param_file(directory_upload_PARAM_beam_align_h,
                                                                     filename_upload_PARAM_beam_align_h,
                                                                     file_extension_upload_PARAM)

    # Lauch analysis
    b_a_h.beam_align_h_analysis(parameters_beam_align_h)
