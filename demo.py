import argparse

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import abp.spherical3d.pairdistribution as abp3dpdf

# -- Parse args --

parser = argparse.ArgumentParser(
    description=r"""Display the pair distribution function for a given
        particle distance, Peclet number and packing density and
        one fixed angle at a certain value.
        The default values are the same as in Fig. 4 of the accompanying
        article by S. Broeker, M. te Vrugt, J. Jeggle and R. Wittkowski.
        """,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "-r", metavar="dist", dest="dist", type=float, default=1.0,
    help="Particle distance in multiples of sigma")
parser.add_argument(
    "-d", metavar="Phi", dest="Phi", type=float, default=0.2,
    help="Packing density")
parser.add_argument(
    "-p", metavar="peclet", dest="peclet", type=float, default=100.0,
    help="Peclet number")
parser.add_argument(
    "-a", metavar="fixed_angle", dest="fixed_angle",  default="the1",
    choices=["the1", "the2", "phi2"],
    help="The angle to be fixed")
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--angle-degrees", metavar="value_fixed_angle_degree",
    dest="value_fixed_angle_degree",
    type=float, default=0,
    help="Value of the fixed angle in degree")
group.add_argument(
    "--angle-radians", metavar="value_fixed_angle_rad", dest="value_fixed_angle_rad",
    type=float, default=0,
    help="Value of the fixed angle in rad(default: 0)")

args = parser.parse_args()

# Validate args
r_min = 0.7775
r_max = 2**(1/6)
if args.dist < r_min or args.dist > r_max:
    print("Warning: Distance is outside of approximation bounds!")
if args.peclet < 0:
    print("Warning: Unphysical argument for Peclet number")
if args.Phi < 0 or args.Phi > 1:
    print("Warning: Unphysical argument for packing density")

# -- Calculate pair distribution function --

# Unify angle parameters to one angle in radians
if args.value_fixed_angle_rad != 0:
    fixed_angle_rad = args.value_fixed_angle_rad
    angle_value_string = str(args.value_fixed_angle_rad)
elif args.value_fixed_angle_degree != 0:
    fixed_angle_rad = np.deg2rad(args.value_fixed_angle_degree)
    angle_value_string = rf"${args.value_fixed_angle_degree}^\circ$"
else:
    fixed_angle_rad = 0.0
    angle_value_string = "0"

# Generate arrays for the1, the2 and phi2
RESOLUTION = 180
the1 = np.linspace(0, 2*np.pi, RESOLUTION, endpoint=False)
the2 = np.linspace(0, 2*np.pi, RESOLUTION, endpoint=False)
phi2 = np.linspace(0, 2*np.pi, RESOLUTION, endpoint=False)

# Replace array for fixed angle
if args.fixed_angle == "the1":
    the1 = fixed_angle_rad
if args.fixed_angle == "the2":
    the2 = fixed_angle_rad
if args.fixed_angle == "phi2":
    phi2 = fixed_angle_rad

# Just take a single distance
r = args.dist  

# Calculate -gU' and squeeze to 2D array
gU = abp3dpdf.reconstruct_gUprime(r, the1, the2, phi2, args.Phi, args.peclet)
gU = np.squeeze(gU)

# Divide by U' to obtain the pair-distribution function g
g = -gU/abp3dpdf.getUprime(args.dist)

# -- Plotting code --

# Set plot labels
if args.fixed_angle == "the1":
    # g = g[angle_index, :, :]
    xlabel = r"$\theta_2$"
    ylabel = r"$\phi_2$"
    caption = r"$\theta_1$"

elif args.fixed_angle == "the2":
    # g = g[:, angle_index, :]
    xlabel = r"$\theta_1$"
    ylabel = r"$\phi_2$"
    caption = r"$\theta_2$"
elif args.fixed_angle == "phi2":
    # g = g[:, :, angle_index]
    xlabel = r"$\theta_1$"
    ylabel = r"$\theta_2$"
    caption = r"$\phi_2$"

caption = caption + " = "+angle_value_string

# Create plot
fig, ax = plt.subplots(1)

g = np.roll(g, 90, 0)
cax = ax.imshow(g.T, cmap="inferno", origin="lower",
                extent=(0, g.shape[0], 0, g.shape[0]), vmin=0)
cbar = fig.colorbar(cax)

cbar.set_label("$g$")

ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)

ax.set_xticks([0, g.shape[0]//2, g.shape[0]])
ax.set_xticklabels([r"$-\pi$", r"0", r"$\pi$"])
ax.xaxis.set_minor_locator(MultipleLocator(g.shape[0]//4))

ax.set_yticks([0, g.shape[0]//2, g.shape[0]])
ax.set_yticklabels(["0", r"$\pi$", r"$2\pi$"])
ax.yaxis.set_minor_locator(MultipleLocator(g.shape[0]//4))

plt.title(caption)
plt.show()
