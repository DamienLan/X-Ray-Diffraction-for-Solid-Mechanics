# -*- coding: utf-8 -*-
"""
X-Ray Diffraction for Solid Mechanics

Author: Olivier Castelnau (olivier.castelnau@ensam.eu), lab PIMM (CNRS UMR8006) at ENSAM Paris, France.
        Vincent MICHEL (vincent.michel@ensam.eu)
        Damien LANASPEZE (damien.lanaspeze@mines-paristech.fr)

Program for the alignment of diffractometers with 1d detector:
    perform an CHI scan for a fixed detector position (while omega=cst) and measure
    the Bragg peak displacement. Then estimate the vertical beam misalignment
    to be corrected.
"""


import time

from modules import b_a_v
from utils import parameters_files


# Common parameters
pixsize = 0.14  # mm
R = 295  # mm

# Analysis parameters

# .TTX file informations
directory = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\experiments\psi_scan'
filename = 'sin2psi_20'
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
xmin = 820
xmax = 880

# Size of the background window for each side of the peak
size_window_background_left = 10
size_window_background_right = 10

# Saving Parameters on .PARAM file
save_PARAMfile_beam_align_v = True
# .PARAM file information
directory_PARAM_beam_align_v = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\parameters'
filename_PARAM_beam_align_v = time.strftime("%d_%B_%Y") + '_beam_align_v'
file_extension_PARAM_beam_align_v = '.PARAM'

# Uploading prameters from a .PARAM file (!! the parameters use by the pragram will not be the previous parameters !!)
upload_PARAM_file = False
directory_upload_PARAM_beam_align_v = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\parameters'
filename_upload_PARAM_beam_align_v = '24_April_2020' + '_beam_align_v'
file_extension_upload_PARAM = '.PARAM'

# Uptating dictionnary
parameters_beam_align_v = dict()
parameters_beam_align_v["pixsize"] = pixsize
parameters_beam_align_v["goniometric_ray"] = R
parameters_beam_align_v["directory_beam_align_v"] = directory
parameters_beam_align_v["filename_beam_align_v"] = filename
parameters_beam_align_v["file_extension_beam_align_v"] = file_extension
parameters_beam_align_v["display_before_removing_beam_align_v"] = display_before_removing
parameters_beam_align_v["image_to_remove_beam_align_v"] = image_to_remove
parameters_beam_align_v["display_after_removing_beam_align_v"] = display_after_removing
parameters_beam_align_v["directory_clean_beam_align_v"] = directory_clean
parameters_beam_align_v["filename_clean_beam_align_v"] = filename_clean
parameters_beam_align_v["file_extension_clean_beam_align_v"] = file_extension_clean
parameters_beam_align_v["save_clean_file_beam_align_v"] = save_clean_file
parameters_beam_align_v["window_xmin_beam_align_v"] = xmin
parameters_beam_align_v["window_xmax_beam_align_v"] = xmax
parameters_beam_align_v["size_window_background_left_beam_align_v"] = size_window_background_left
parameters_beam_align_v["size_window_background_right_beam_align_v"] = size_window_background_right

if __name__ == '__main__':

    if save_PARAMfile_beam_align_v:
        parameters_files.save_param_file(parameters_beam_align_v,
                                         directory_PARAM_beam_align_v,
                                         filename_PARAM_beam_align_v,
                                         file_extension_PARAM_beam_align_v)

    if upload_PARAM_file:
        parameters_beam_align_v = parameters_files.upload_param_file(directory_upload_PARAM_beam_align_v,
                                                                     filename_upload_PARAM_beam_align_v,
                                                                     file_extension_upload_PARAM)

    # Lauch analysis
    b_a_v.beam_align_v_analysis(parameters_beam_align_v)
