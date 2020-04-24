# -*- coding: utf-8 -*-
"""
Define function for read and write .CALI file
"""


def read_data_CALI(directory_cali, filename_cali, extension_cali='.CALI'):
    """
    Read .CALI file
    """
    # read the .CALI file
    name_cali = directory_cali + '\\' + filename_cali + extension_cali

    try:
        with open(name_cali, 'r') as file:
            data = file.readlines()

    except FileNotFoundError:
        print('Lecture fichier CALI : Fichier introuvable')

    else:
        # getting poni, alpha_med and alpha_pix
        line = [ln.split() for ln in data]
        correction_pix = []
        for ii in range(5, len(line)):
            correction_pix.append(float(line[ii][1]))

        return correction_pix


def write_data_CALI(correction_pix, directory, filename, extension='.CALI'):
    """
    Write a .CALI file giving the correction angle for each pixel
    """

    # getting the name
    name = directory + '\\' + filename + extension

    try:
        # create the file
        file = open(name, "w+")

    except FileNotFoundError:
        print('Ecriture fichier CALI : Dossier introuvable')

    else:
        # heading text
        file.write('file             : ' + name + '\n')
        file.write('\nCalibration of Inel detector\n')

        # write data
        file.write('\nangle correction in function of the pixel\n')
        for ii in range(len(correction_pix)):
            file.write(f'  {ii + 1}     {correction_pix[ii]:5.4e}\n')

        file.close()

