# -*- coding: utf-8 -*-
"""
X-Ray Diffraction for Solid Mechanics

Author: Olivier Castelnau (olivier.castelnau@ensam.eu), lab PIMM (CNRS UMR8006) at ENSAM Paris, France.
        Vincent MICHEL (vincent.michel@ensam.eu)
        Damien LANASPEZE (damien.lanaspeze@mines-paristech.fr)

Fit data for finding the position of the center of rotation of a goniometer.
"""


import time
import numpy as np

from modules import g_c
from utils import parameters_files


# Common parameters
pixsize = 0.14  # mm
R = 295  # mm

# Analysis parameters

# ray (not diameter!) of the comparator tip, in [mm]
rtip = 0.515

# Enter the value of the angle (omega or chi) in [deg], and the value read on the comparator (in [mm])
alpha = np.array([-5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
z = np.array([4.767, 4.767, 4.775, 4.780, 4.785, 4.7875, 4.789, 4.786, 4.780, 4.770, 4.750])

# Initials guess for the fit [mm]
e = 0
z0 = 0

# MinMax values
e_max = 10
z0_max = 20

# Saving Parameters on .PARAM file
save_PARAMfile_gonio_center = True
directory_PARAM_gonio_center = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\parameters'
filename_PARAM_gonio_center = time.strftime("%d_%B_%Y") + '_gonio_center'
file_extension_PARAM_gonio_center = '.PARAM'

# Uploading prameters from a .PARAM file (!! the parameters use by the pragram will not be the previous parameters !!)
upload_PARAM_file = False
directory_upload_PARAM_gonio_center = r'D:\Damien\Scolaire\3.Mines\2A\S3R\XRDSM\data\parameters'
filename_upload_PARAM_gonio_center = '24_April_2020' + '_gonio_center'
file_extension_upload_PARAM = '.PARAM'

# Uptating dictionnary
parameters_gonio_center = dict()
parameters_gonio_center["pixsize"] = pixsize
parameters_gonio_center["goniometric_ray"] = R
parameters_gonio_center["rtip_gonio_center"] = rtip
parameters_gonio_center["alpha_gonio_center"] = alpha
parameters_gonio_center["z_gonio_center"] = z
parameters_gonio_center["e_gonio_center"] = e
parameters_gonio_center["z0_gonio_center"] = z0
parameters_gonio_center["e_max_gonio_center"] = e_max
parameters_gonio_center["z0_max_gonio_center"] = z0_max

if __name__ == '__main__':

    if save_PARAMfile_gonio_center:
        parameters_files.save_param_file(parameters_gonio_center,
                                         directory_PARAM_gonio_center,
                                         filename_PARAM_gonio_center,
                                         file_extension_PARAM_gonio_center)

    if upload_PARAM_file:
        parameters_gonio_center = parameters_files.upload_param_file(directory_upload_PARAM_gonio_center,
                                                                     filename_upload_PARAM_gonio_center,
                                                                     file_extension_upload_PARAM)

    # Lauch analysis
    g_c.gonio_center_analysis(parameters_gonio_center)
