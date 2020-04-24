# -*- coding: utf-8 -*-
"""
X-Ray Diffraction for Solid Mechanics

Author: Olivier Castelnau (olivier.castelnau@ensam.eu), lab PIMM (CNRS UMR8006) at ENSAM Paris, France.
        Vincent MICHEL (vincent.michel@ensam.eu)
        Damien LANASPEZE (damien.lanaspeze@mines-paristech.fr)

Using a .CALI file and a .TTX file, get the image of one or some acquisition
"""


import time

from modules import r_i
from utils import parameters_files


# Common parameters
pixsize = 0.14  # mm
R = 295  # mm

# Analysis parameters

# .TTX file informations
directory = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\experiments\LaB6'
filename = '2019-10-11 Tube Cu - 20_150_pas de 5'
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

# .CALI file information (reading .CALI file)
directory_CALI = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\calibration'
filename_CALI = '2019-11-20 Scan FD_clean'
file_extension_CALI = '.CALI'

# Saving Parameters on .PARAM file
save_PARAMfile_read_image = False
dictionnary_name_read_image = 'read_image_parameters'
directory_PARAM_read_image = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\parameters'
filename_PARAM_read_image = time.strftime("%d_%B_%Y") + '_read_image'
file_extension_PARAM_read_image = '.PARAM'

# Uploading prameters from a .PARAM file (!! the parameters use by the pragram will not be the previous parameters !!)
upload_PARAM_file = True
directory_upload_PARAM_read_image = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\parameters'
filename_upload_PARAM_read_image = '24_April_2020' + '_read_image'
file_extension_upload_PARAM = '.PARAM'

# Uptading dictionnary
parameters_read_image = dict()
parameters_read_image["pixsize"] = pixsize
parameters_read_image["goniometric_ray"] = R
parameters_read_image["directory_read_image"] = directory
parameters_read_image["filename_read_image"] = filename
parameters_read_image["file_extension_read_image"] = file_extension
parameters_read_image["display_before_removing_read_image"] = display_before_removing
parameters_read_image["image_to_remove_read_image"] = image_to_remove
parameters_read_image["display_after_removing_read_image"] = display_after_removing
parameters_read_image["directory_clean_read_image"] = directory_clean
parameters_read_image["filename_clean_read_image"] = filename_clean
parameters_read_image["file_extension_clean_read_image"] = file_extension_clean
parameters_read_image["save_clean_file_read_image"] = save_clean_file
parameters_read_image["directory_CALI_read_image"] = directory_CALI
parameters_read_image["filename_CALI_read_image"] = filename_CALI
parameters_read_image["file_extension_CALI_read_image"] = file_extension_CALI
parameters_read_image["pixsize"] = pixsize
parameters_read_image["goniometric_ray"] = R

if __name__ == '__main__':

    if save_PARAMfile_read_image:
        parameters_files.save_param_file(parameters_read_image,
                                         directory_PARAM_read_image,
                                         filename_PARAM_read_image,
                                         file_extension_PARAM_read_image)

    if upload_PARAM_file:
        parameters_read_image = parameters_files.upload_param_file(directory_upload_PARAM_read_image,
                                                                   filename_upload_PARAM_read_image,
                                                                   file_extension_upload_PARAM)

    # Lauch analysis
    r_i.read_image_analysis(parameters_read_image)
