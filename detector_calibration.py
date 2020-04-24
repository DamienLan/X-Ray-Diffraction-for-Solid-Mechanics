# -*- coding: utf-8 -*-
"""
X-Ray Diffraction for Solid Mechanics

Author: Olivier Castelnau (olivier.castelnau@ensam.eu), lab PIMM (CNRS UMR8006) at ENSAM Paris, France.
        Vincent MICHEL (vincent.michel@ensam.eu)
        Damien LANASPEZE (damien.lanaspeze@mines-paristech.fr)
        
Program for the calibration for 1D-detector:
    preform a 2theta scan WITHOUT sample : direct incidence
    scan : 2theta around -12° ==> 2theta around +12°
"""


import time

from modules import d_c
from utils import parameters_files


# Common parameters
pixsize = 0.14  # mm
R = 295  # mm

# Analysis parameters

# .TTX file informations
directory = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\normal_incidence'
filename = '2019-11-20 Scan FD'
file_extension = '.TTX'

# Display before removing : True or False
display_before_removing = False
# Put here the number of the image(s) to remove
l1 = [i for i in range(1, 24)]
l2 = [42, 110, 251]
l3 = [j for j in range(275, 302)]
image_to_remove = l1 + l2 + l3
# Display before removing : True or False
display_after_removing = False

# Save clean file : True or False
save_clean_file = False
# .TTX clean file informations
directory_clean = directory
filename_clean = filename + '_clean'
file_extension_clean = file_extension

# Save .CALI file : True or False
save_CALI = True
# .CALI file information (saving .CALI file)
directory_CALI = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\calibration'
filename_CALI = filename_clean
file_extension_CALI = '.CALI'

# Saving Parameters on .PARAM file
save_PARAMfile_detector_calibration = True
dictionnary_name_detector_calibration = 'detector_calibration_parameters'
directory_PARAM_detector_calibration = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\parameters'
filename_PARAM_detector_calibration = time.strftime("%d_%B_%Y") + '_detector_calibration'
file_extension_PARAM_detector_calibration = '.PARAM'

# Uploading prameters from a .PARAM file (!! the parameters use by the pragram will not be the previous parameters !!)
upload_PARAM_file = False
directory_upload_PARAM_detector_calibration = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\parameters'
filename_upload_PARAM_detector_calibration = '24_April_2020' + '_detector_calibration'
file_extension_upload_PARAM = '.PARAM'

# Uptading dictionnary
parameters_detector_calibration = dict()
parameters_detector_calibration["pixsize"] = pixsize
parameters_detector_calibration["goniometric_ray"] = R
parameters_detector_calibration["directory_detector_calibration"] = directory
parameters_detector_calibration["filename_detector_calibration"] = filename
parameters_detector_calibration["file_extension_detector_calibration"] = file_extension
parameters_detector_calibration["display_before_removing_detector_calibration"] = display_before_removing
parameters_detector_calibration["image_to_remove_detector_calibration"] = image_to_remove
parameters_detector_calibration["display_after_removing_detector_calibration"] = display_after_removing
parameters_detector_calibration["directory_clean_detector_calibration"] = directory_clean
parameters_detector_calibration["filename_clean_detector_calibration"] = filename_clean
parameters_detector_calibration["file_extension_clean_detector_calibration"] = file_extension_clean
parameters_detector_calibration["save_clean_file_detector_calibration"] = save_clean_file
parameters_detector_calibration["directory_CALI_detector_calibration"] = directory_CALI
parameters_detector_calibration["filename_CALI_detector_calibration"] = filename_CALI
parameters_detector_calibration["file_extension_CALI_detector_calibration"] = file_extension_CALI
parameters_detector_calibration["save_CALI_detector_calibration"] = save_CALI
parameters_detector_calibration["pixsize"] = pixsize
parameters_detector_calibration["goniometric_ray"] = R

if __name__ == '__main__':

    if save_PARAMfile_detector_calibration:
        parameters_files.save_param_file(parameters_detector_calibration,
                                         directory_PARAM_detector_calibration,
                                         filename_PARAM_detector_calibration,
                                         file_extension_PARAM_detector_calibration)

    if upload_PARAM_file:
        parameters_detector_calibration = parameters_files.upload_param_file(directory_upload_PARAM_detector_calibration,
                                                                     filename_upload_PARAM_detector_calibration,
                                                                     file_extension_upload_PARAM)

    # Lauch analysis
    d_c.detector_calibration_analysis(parameters_detector_calibration)