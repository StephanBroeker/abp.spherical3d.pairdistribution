# -*- coding: utf-8 -*-

"""Module for approximating the product of the pair distribution function and
the potential derivative for a three-dimensional suspension of active Brownian
particles."""

from ._reconstruct import *
# Trick pdoc3 into documenting submodule contents as members of this module
from ._reconstruct import __all__ as reconstruct_all
__all__ = reconstruct_all

__author__ = "Stephan Bröker, Julian Jeggle, Raphael Wittkowski"
__copyright__ = "Copyright (C) 2022 Stephan Bröker, Julian Jeggle, Raphael Wittkowski"
__license__ = "MIT"
__version__ = "1.0"
