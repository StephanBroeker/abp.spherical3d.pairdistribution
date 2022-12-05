Supplementary materials
=======================
This folder contains supplementary materials for the article

*S. Bröker and R. Wittkowski, Pair-distribution function of
active Brownian particles in three spatial dimensions, [TODO: arXiv link] (2019)*

Contents
--------
* `abp3d/`: Python module for simplified access to the fit parameters of the
Fourier coefficients described in the article as well as routines for
reconstruction of the product of the pair distribution function and the
potential derivative. See below for installation instructions.
The abp3d module includes:
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
* `demo.py`: Demo code for the `abp3d` module. See `python3 demo.py -h` for more
information.
* `doc/`: HTML documentation for the `abp3d` module.
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

To install the Python module, copy or link the folder `abp3d` to a location in
your Python search path. You can find all locations in your search path by
running:

```bash
python3 -c "import sys; print('\n'.join(sys.path))"
```
