Python module abp.spherical3d.pairdistribution
=======================
This folder contains supplementary software for the article

*S. Bröker, M. te Vrugt, J. Jeggle, J. Stenhammar and R. Wittkowski, Pair-distribution function of
active Brownian spheres in three spatial dimensions: simulation results and analytical represantation, [TODO: arXiv link] (2023)*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8177216.svg)](https://doi.org/10.5281/zenodo.8177216)

Contents
--------
* `abp/spherical3d/pairdistribution`: Python module for simplified access to the fit parameters of the
Fourier coefficients described in the article as well as routines for
reconstruction of the product of the pair distribution function and the
potential derivative. See below for installation instructions.
The abp module includes:
-loadParameterFile         
    this function loads the CSV file from a given path
-reconstruct_gUprime
    Returns an approximation for -gU' in a given range of particle distances and
    positional and orientational angles.
-reconstruct_gUprime_vectors  
    Returns an approximation for -gU' in a given range of particle
    distances and orientation of the particles and their connecting vector
-getUprime
    Calculate derivative of potential U with respect to r                
* `demo.py`: Demo code for the `abp` module. See `python3 demo.py -h` for more
information.
* `doc/`: HTML documentation for the `abp` module.
* `fitparams.csv`: Spreadsheet file containing all fit parameters for the
Fourier coefficients described in the article.
* `README.md`: This file.

Installation
------------
Reasonably recent versions of the following software are required to make use of
the supplied code:
* Python 3
* NumPy
* Matplotlib (needed for the demo script)

To install the Python module, copy or link the folder `abp` to a location in
your Python search path. You can find all locations in your search path by
running:

```bash
python3 -c "import sys; print('\n'.join(sys.path))"
```
