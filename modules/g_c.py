# -*- coding: utf-8 -*-
"""
Fit data for finding the position of the center of rotation of a goniometer.
"""


import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


# Goniometer function
def gonio_center(alpha, *param):
    e, rtip, z0 = param
    z = (e + rtip) / np.cos(alpha * np.pi / 180) + z0
    return z


def gonio_center_analysis(dic):
    """
    Gonio center analysis using parameters stored in the dic
    """
    rtip = dic["rtip_gonio_center"]
    alpha = dic["alpha_gonio_center"]
    z = dic["z_gonio_center"]
    e = dic["e_gonio_center"]
    z0 = dic["z0_gonio_center"]
    e_max = dic["e_max_gonio_center"]
    z0_max = dic["z0_max_gonio_center"]

    popt, pcov = curve_fit(gonio_center, alpha, z, p0=[e, rtip, z0],
                           bounds=([-e_max, rtip, -z0_max], [e_max, rtip + 1.e-6, z0_max]))

    print()
    print(f'Rayon de la pointe du comparateur : {rtip:.3f} mm')
    print(f'Parametres optimises : e = {popt[0]:.3f} mm, z0 = {popt[2]:.3f} mm')
    print()
    print(f'Le centre de rotation du gonio devrait se situer à z = {popt[2] + rtip:.3f} mm.')

    # plot
    fig, ax = plt.subplots(figsize=(7, 4))
    # plot data
    ax.plot(alpha, z, 'b.', label='data', markersize=3)
    ax.set_title(f'Goniometric center, e = {popt[0]:.3f} mm, z0 = {popt[2]:.3f} mm')
    ax.set_xlabel('Angle [deg]')
    ax.set_ylabel('Position [mm]')
    # plot fit
    x = np.arange(np.min(alpha) * 1.1, np.max(alpha) * 1.1, 1.)
    ax.plot(x, gonio_center(x, *popt), '-r', label='fit', linewidth=0.5)
    plt.legend()
    # fig.savefig('_gonio_center'+'.png', dpi=300)
    plt.show()
