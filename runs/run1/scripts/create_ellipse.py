"""
Creates an ellipse and regularizes it.
"""

import sys
import numpy
import pathlib
from matplotlib import pyplot


root_dir = pathlib.Path(__file__).absolute().parents[3]
module_dir = root_dir / 'src/python'
if module_dir not in sys.path:
  sys.path.insert(0, str(module_dir))
from regularize import regularize


def ellipse(a, b, center=(0.0, 0.0), num=50):
    """
    Returns the coordinates of an ellipse.

    Parameters
    ----------
    a: float
        The semi-major axis of the ellipse.
    b: float
        The semi-minor axis of the ellipse.
    center: 2-tuple of floats, optional
        The position of the center of the ellipse;
        default: (0.0, 0.0)
    num: integer, optional
        The number of points on the upper side of the ellipse.
        The number includes the leading and trailing edges.
        Thus, the total number of points will be 2 * (num - 1);
        default: 50.

    Returns
    -------
    x: numpy.ndarray of floats
        The x-coordinates of the ellipse.
    y: numpy.ndarray of floats
        The y-coordinates of the ellipse.
    """
    xc, yc = center
    x_upper = numpy.linspace(xc + a, xc - a, num=num)
    y_upper = b / a * numpy.sqrt(a**2 - x_upper**2)
    x_lower = numpy.linspace(xc - a, xc + a, num=num)[1:-1]
    y_lower = -b / a * numpy.sqrt(a**2 - x_lower**2)
    x = numpy.concatenate((x_upper, x_lower))
    y = numpy.concatenate((y_upper, y_lower))
    return x, y


# Define main directory.
root_dir = pathlib.Path(__file__).absolute().parents[1]

# Set the type and size of the font to use in Matplotlib figures.
pyplot.rc('font', family='serif', size=16)

# Set parameters of the ellipse.
c = 1.0  # chord of the ellipse (major axis)
r = 0.10  # ratio between minor and major axis
a, b = c / 2.0, r * c / 2.0
x0, y0 = ellipse(a, b, center=(0.0, 0.0), num=100)

# Regularize the boundary given a resolution.
ds = 0.025  # target distance between two consecutive points.
x, y = regularize(x0, y0, ds=ds)

# Plot the ellipse.
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.grid()
ax.plot(x0, y0, color='C0', linestyle='-', linewidth=2, marker='o')
ax.plot(x, y, color='C1', linestyle='--', linewidth=2, marker='x')
ax.axis('scaled', adjustable='box')
ax.set_xlim(-0.75, 0.75)
ax.set_ylim(-0.25, 0.25)
pyplot.show()

# Write coordinates into a file.
filepath = root_dir / 'ellipse.body'
with open(filepath, 'w') as outfile:
    outfile.write('{}\n'.format(x.size))
with open(filepath, 'ab') as outfile:
    numpy.savetxt(outfile, numpy.c_[x, y])
