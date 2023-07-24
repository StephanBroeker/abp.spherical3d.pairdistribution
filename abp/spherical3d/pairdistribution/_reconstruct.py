#!/usr/bin/env python3

import os.path
import numpy as np

from .fitfuncs import FOURIERFITFUNCS, PARAMETERFITFUNCS

__all__ = ["loadParameterFile", "reconstruct_gUprime",
           "getUprime", "reconstruct_gUprime_vectors"]

# -- Internal constants for loading the default parameter file --

SCRIPTDIR = os.path.dirname(os.path.abspath(__file__))
FITPARAMSFILE = "fitparams.csv"
DEFAULTPATH = os.path.join(SCRIPTDIR, FITPARAMSFILE)
DEFAULTPARAMETERS = None  # Lazy loading: will be set when needed

# -- Simulation constants --

EPSILON, SIGMA = 1, 1

# -- File input --


def loadParameterFile(filepath):
    r"""Load a parameter CSV file from a given path.

    Args:
        path (str):
            Path to CSV file.

    Returns:
        **params_alpha, params_beta (dict):**
            Dictionaries containing all fit parameters for both alpha and beta
            Fourier coefficients.
    """
    params_alpha = {}
    params_beta = {}
    # Open file with fit parameters and read line by line every u_i,j
    # or v,w resp.
    with open(filepath) as f:
        for line in f:
            # Extract cells
            cells = line.split(",")
            # Skip lines without label
            if cells[0] == "":
                continue
            # Skip invalid labels
            if not len(cells[0]) in [8, 9]:
                print("Invalid fourier coefficient label: {}".format(cells[0]))
                continue
            coefftype = cells[0][0:4]  # Either "alph" or "beta"

            h, j, k = map(int, cells[0][-3:])

            # Select correct dict
            params = params_alpha if coefftype == "alph" else params_beta

            # Filter empty cells
            cells = list(filter(lambda x: x != "", cells))
            if not (h, j, k) in params:
                params[(h, j, k)] = []
            # Extract data
            params[(h, j, k)].append(list(map(float, cells[2:])))
        return params_alpha, params_beta

# Internally used


def loadDefaultParameterFile():
    global DEFAULTPARAMETERS
    if not DEFAULTPARAMETERS:
        DEFAULTPARAMETERS = loadParameterFile(DEFAULTPATH)
    return DEFAULTPARAMETERS

# -- Reconstruction functions --


def reconstruct_gUprime(
        r, the1, the2, phi2, Phi, Pe, params_alpha=None, params_beta=None):
    #    r, phi1, phi2, phi0, Pe, params_alpha=None, params_beta=None):
    r"""Returns an approximation for $-gU'$ in a given range of particle
    distances and positional and orientational angles.

    Args:
        r (float or array_like): Distance(s) at which $-gU'$ will be calculated
        the1, the2, phi2 (float, array_like or meshgrid of all):
            Positional and orientational angles at which $-gU'$ will be calculated
        Phi, Pe (float): Packing density and Peclet number for which $-gU'$ will be calculated
        params_alpha, params_beta (dict):
            Parameter dictionary containing all fit parameters necessary for
            reconstruction. If not set, the included default values will be used.
    """
    # If params are not set: load default
    if not params_alpha or not params_beta:
        params = loadDefaultParameterFile()
        if not params_alpha:
            params_alpha = params[0]
        if not params_beta:
            params_beta = params[1]
    # r must have dimension 1
    if len(np.shape(r)) == 0:
        r = np.array([r])

    # Allocate array for -gU'
    if len(np.shape(the1)) == 3 and len(np.shape(the2)) == 3 and \
            len(np.shape(phi2)) == 3:
        pass
    elif len(np.shape(the1)) in [0, 1] and len(np.shape(the2)) in [0, 1] and \
            len(np.shape(phi2)) in [0, 1]:
        the1, the2, phi2 = np.meshgrid(the1, the2, phi2, indexing='ij')
    else:
        print("""I dont know how to interpret the input of the1, the2 and phi2.\n
        Please either give only onedimensional arrays or floats""" + """ \
             as input or give only meshgrids. """)

    gU = np.zeros((r.shape[0], the1.shape[0], the2.shape[1], phi2.shape[2]))

    # Calculate all contributions for h,j,k between 0 and 2

    for k in range(3):
        # cos*cos*cos for h,j,k of alpha coefficient
        # sin*sin*cos for h,j,k of beta coefficient
        phi2_func = np.cos
        lowest_freq = 0
        fourierfunc = np.cos
        if k == 1:
            lowest_freq = 1
            fourierfunc = np.sin
        for h in range(lowest_freq, 3, 1):
            for j in range(lowest_freq, 3, 1):

                for params in (
                        [params_beta] if k == 1 else
                        [params_alpha]):
                    # Calculate fit parameters a, mu, sigma, lambda and b,c,d
                    # (if necessary)
                    fitparams = list(map(lambda x: x[0]((Phi, Pe), *x[1]),
                                     zip(PARAMETERFITFUNCS[(h, j, k)],
                                     params[(h, j, k)])))
                    # Calculate Fourier coefficient
                    fouriercoeff = FOURIERFITFUNCS[(h, j, k)](r, *fitparams)
                    # Add contribution to -gU'
                    gU += fouriercoeff[:, None, None, None] * \
                        fourierfunc(the1*h) * fourierfunc(the2*j) * \
                        phi2_func(phi2*k)

    return gU


def reconstruct_gUprime_vectors(
     r, u_1, u_2, u_d, Phi, Pe, params_alpha=None, params_beta=None):
    r"""Returns an approximation for $-gU'$ in a given range of particle
    distances and orientation of the particles and their connecting vector.

    Args:
        r (float): Distance(s) at which $-gU'$ will be calculated
        u_1, u_2, u_d (array-like, dimension 3):
            Normalized orientation vectors of the particles and
            their connecting vector
        Phi, Pe (float):
            Packing density and Peclet number for which $-gU'$ will
            be calculated
        params_alpha, params_beta (dict):
            Parameter dictionary containing all fit parameters necessary for
            reconstruction. If not set, the included default values will be used.
    """
    # in case u_ are lists, this changes them to arrays
    # u_1 = np.array([u_1[0], u_1[1],u_1[2]])
    # u_2 = np.array([u_2[0], u_2[1],u_2[2]])
    # u_d = np.array([u_d[0], u_d[1],u_d[2]])

    # normalizing the vectors
    u_1 = u_1/np.sqrt(np.sum(u_1*u_1))
    u_2 = u_2/np.sqrt(np.sum(u_2*u_2))
    u_d = u_d/np.sqrt(np.sum(u_d*u_d))

    # Calculation of the angles the1, the2 and phi2
    u1_u2 = np.sum(u_1*u_2)
    u1_ud = np.sum(u_1*u_d)
    the1 = np.arccos(u1_ud)
    the2 = np.arccos(u1_u2)

    # for certain configurations of u1 and u2, phi2 can be chosen arbitrarly
    limit = np.cos(np.pi/180)
    if abs(u1_u2) > limit or abs(u1_ud) > limit:
        phi2 = 0.0
    else:
        ey = np.cross(u_1, u_d)
        ey = ey/np.sqrt(np.sum(ey*ey))
        ex = np.cross(ey, u_1)
        phi2 = np.arccos(np.sum(u_2*ex)/np.sqrt(1-u1_u2*u1_u2))

    return reconstruct_gUprime(
            r, the1, the2, phi2, Phi, Pe, params_alpha=None, params_beta=None)


def getUprime(r):
    r"""Calculate derivative of potential U with respect to r.

    The potential depends on the particle diameter sigma and the Lennard-Jones
    energy epsilon. This function uses values consistent with the simulations
    described in the accompanying article.

    Args:
        r (float or array_like):
            Distance(s) at which the potential derivative will be calculated.
    """
    return 24*EPSILON/SIGMA * (-2*(SIGMA/r)**13 + (SIGMA/r)**7)
