"""Functions for both fitting procedures of the Fourier coefficients of -gU'.

For the functions of the first fitting procedure the order of arguments matches
the one shown in the row headers for each Fourier coefficient in fitparams.csv.
Likewise for the functions of the second fitting procedure matches the order of
arguments shown in the header line in fitparams.csv."""

from numpy import sqrt, exp
from scipy.special import erfc

# -- Functions for first fitting procedure --


def EMG(r, mu, sig, la):
    """Exponentially modified Gaussian distribution."""
    return la/2 * exp(la/2 * (la*sig**2 - 2*(r-mu))) * \
        erfc((la*sig**2 - (r-mu))/sqrt(2)/sig)


def FourierFit0(r, a, mu, sig, la):
    """Function for first fitting procedure with one fixed root."""
    return a*EMG(r, mu, sig, la) * (2**(1/6) - r)


def FourierFit1(r, a, mu, sig, la, b):
    """Function for first fitting procedure with one fixed and one variable
    root."""
    return FourierFit0(r, a, mu, sig, la) * (b-r)


def FourierFit2(r, a, mu, sig, la, b, c):
    """Function for first fitting procedure with one fixed and two variable
    roots."""
    return FourierFit1(r, a, mu, sig, la, b) * (c-r)


def FourierFit3(r, a, mu, sig, la, b, c):
    """Function for first fitting procedure with one fixed and one variable
    root."""
    return FourierFit0(r, a, mu, sig, la) * (r**2+b*r+c)


def FourierFit4(r, a, mu, sig, la, b, c, d):
    """Function for first fitting procedure with one fixed and one variable
    root."""
    return FourierFit3(r, a, mu, sig, la, b, c) * (d-r)

FOURIERFITFUNCS = {
    (0, 0, 0): FourierFit0,
    (0, 0, 2): FourierFit1,
    (0, 1, 0): FourierFit1,
    (0, 1, 2): FourierFit2,
    (0, 2, 0): FourierFit3,
    (0, 2, 2): FourierFit1,
    (1, 0, 0): FourierFit1,
    (1, 0, 2): FourierFit2,
    (1, 1, 0): FourierFit1,
    (1, 1, 2): FourierFit4,
    (1, 2, 0): FourierFit2,
    (1, 2, 2): FourierFit2,
    (2, 0, 0): FourierFit1,
    (2, 0, 2): FourierFit1,
    (2, 1, 0): FourierFit1,
    (2, 1, 2): FourierFit2,
    (2, 2, 0): FourierFit1,
    (2, 2, 2): FourierFit1,
    (1, 1, 1): FourierFit1,
    (1, 2, 1): FourierFit2,
    (2, 1, 1): FourierFit1,
    (2, 2, 1): FourierFit1
}
""" Dictionary mapping the index triple (h,k,l)
    to the corresponding fit function"""

# -- Functions for second fitting procedure --


def h(x, u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15,
        u16, u17, u18, u19, u20):
    """Function h for second fitting procedure."""
    dens, Pe = x
    return \
        (u1 /Pe + u2 /sqrt(Pe) + u3  + u4 *sqrt(Pe) + u5 *Pe) + \
        (u6 /Pe + u7 /sqrt(Pe) + u8  + u9 *sqrt(Pe) + u10*Pe)*dens + \
        (u11/Pe + u12/sqrt(Pe) + u13 + u14*sqrt(Pe) + u15*Pe)*dens**2 +  \
        (u16/Pe + u17/sqrt(Pe) + u18 + u19*sqrt(Pe) + u20*Pe)*dens**3


PARAMETERFITFUNCS = {
    (0, 0, 0): [h, h, h, h],
    (0, 0, 2): [h, h, h, h, h],
    (0, 1, 0): [h, h, h, h, h],
    (0, 1, 2): [h, h, h, h, h, h],
    (0, 2, 0): [h, h, h, h, h, h],
    (0, 2, 2): [h, h, h, h, h],
    (1, 0, 0): [h, h, h, h, h],
    (1, 0, 2): [h, h, h, h, h, h],
    (1, 1, 0): [h, h, h, h, h],
    (1, 1, 2): [h, h, h, h, h, h, h],
    (1, 2, 0): [h, h, h, h, h, h],
    (1, 2, 2): [h, h, h, h, h, h],
    (2, 0, 0): [h, h, h, h, h],
    (2, 0, 2): [h, h, h, h, h],
    (2, 1, 0): [h, h, h, h, h],
    (2, 1, 2): [h, h, h, h, h, h],
    (2, 2, 0): [h, h, h, h, h],
    (2, 2, 2): [h, h, h, h, h],
    (1, 1, 1): [h, h, h, h, h],
    (1, 2, 1): [h, h, h, h, h, h],
    (2, 1, 1): [h, h, h, h, h],
    (2, 2, 1): [h, h, h, h, h]
}
"""Dictionary mapping the index triple (h,k,l) to an array of fit functions for
each fit parameter of FourierFit{0,1,2,3,4}."""
