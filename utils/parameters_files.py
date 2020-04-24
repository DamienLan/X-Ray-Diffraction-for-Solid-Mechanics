# -*- coding: utf-8 -*-
"""
Define two functions for save and upload parameter dictionnary
"""


import pickle


def save_param_file(dic, directory, filename, file_extension='.PARAM'):
    """
    Save a parameter dictionnary in a file
    """

    # Getting the name of the new file
    name = directory + '\\' + filename + file_extension
    # Creating the file
    file = open(name, "wb+")

    pickler = pickle.Pickler(file)
    pickler.dump(dic)

    print('Parameters saved')


def upload_param_file(directory, filename, file_extension='.PARAM'):
    """
    Upload parameter dictionnary
    """
    # Obtaining file name
    name = directory + '\\' + filename + file_extension

    try:
        with open(name, 'rb') as file:
            unpickler = pickle.Unpickler(file)
            dic = unpickler.load()

    except FileNotFoundError:
        print('Chargement parametres : Fichier introuvable')

    else:
        print('Parameters uploaded')
        return dic
