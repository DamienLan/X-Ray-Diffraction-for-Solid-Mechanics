# -*- coding: utf-8 -*-
"""
Define function for read and write Seifert datafile .TTX
"""


def read_seifert_data_TTX(directory, filename, extension='TTX'):
    """
    Read .ttx files.
    Returns:
        tth : list of 2theta angle
        omega : list of omega angle
        chi : list of chi angle
        phi : list of phi angle
        intensity: list of (list of intensity for each pixel) for each acquisition
    """
    # Declaration
    tth = []
    omega = []
    chi = []
    phi = []
    intensity = []

    # Obtaining file name
    name = directory + '\\' + filename + extension

    # Reading of the file

    try:
        with open(name, 'r') as file:
            data = file.readlines()

    except FileNotFoundError:
        print('Lecture seifert data TTX : Fichier introuvable')

    else:
        # Obtaining list of line
        line = [ln.split() for ln in data]

        # Obtaining number of pixel for one acquisition
        number_of_point = int(line[1][4])

        # Temporary variables
        acquisition = []
        temp = []

        # Separation of each acquisition
        for elem in line:
            if elem[0] == '********************************':
                acquisition.append(temp)
                temp = []
            else:
                temp.append(elem)

        # Append of the last "temp" acquisition
        acquisition.append(temp)

        # Deletion of the first element : date, name of the file...
        acquisition.pop(0)

        # Obtaining each angles and intensity for each acquisition
        for acqui in acquisition:

            intensity_one_acquisition = []

            for pixel in range(3, 2 + (number_of_point + 1)):
                intensity_one_acquisition.append(float(acqui[pixel][1]))

            tth.append(float(acqui[1][0]))
            omega.append(float(acqui[1][1]))
            chi.append(float(acqui[1][2]))
            phi.append(float(acqui[1][6]))
            intensity.append(intensity_one_acquisition)

        return tth, omega, chi, phi, intensity


def write_seifert_data_TTX(tth, omega, chi, phi, cts, directory, filename, extension='.TTX'):
    """
    Write .TTX file
    """

    # read angle detector in a data file
    directory_angle = r'..\data\INEL_detector'
    filename_angle = 'angle_detector'
    file_extension_angle = '.txt'

    name_angle = directory_angle + '\\' + filename_angle + file_extension_angle

    try:
        with open(name_angle, 'r') as file:
            l_detector = file.readlines()
            liste_detector = [elem[2:len(elem) - 3] for elem in l_detector]

    except FileNotFoundError:
        print('Ecriture seifert data TTX : Fichier référence introuvable')

    else:
        # défault value for acquisition time
        acq_time = str(300)
        # getting number of image and point
        number_of_point = len(cts[0])
        number_of_image = len(tth)

        # getting the name
        name = directory + '\\' + filename + extension

        # create the file
        try:
            file = open(name, "w+")

        except FileNotFoundError:
            print('Ecriture fichier seifert : Dossier introuvable')

        else:
            # heading text
            file.write('File             : ' + name + '\n')
            file.write('Number of points :  ' + str(number_of_point) + '\n')
            file.write('  2theta    theta     Chi       X        Y        Z        Phi\n')

            # writing of each acquisition
            for ii in range(number_of_image):
                # heading text for one acquisition
                file.write('********************************\n')
                file.write('Scan Number :     ' + str(ii + 1) + '\n')
                file.write(
                    f'   {tth[ii]:5.3f}    {omega[ii]:5.3f}     {chi[ii]:5.3f}    0.000    0.000    0.000    {phi[ii]:5.3f}\n')
                file.write('Acq time    :   ' + acq_time + '\n')

                # intensity for one acquisition
                for jj in range(number_of_point):
                    file.write('    ' + str(liste_detector[jj]) + '     ' + str(int(cts[ii][jj])) + '\n')

            file.close()
