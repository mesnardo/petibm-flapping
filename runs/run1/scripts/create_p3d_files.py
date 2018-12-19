"""
Create files with 3D coordinates to visualize body in VisIt.
"""

import pathlib
import numpy
import yaml


simu_dir = pathlib.Path(__file__).absolute().parents[1]

# Get the time parameters from configuration file.
filepath = simu_dir / 'config.yaml'
with open(filepath, 'r') as infile:
    config = yaml.load(infile)['parameters']
nstart = config['startStep']
nt = config['nt']
nsave = config['nsave']

# Create a Point3D file of the body at saved time-step.
for n in range(nstart, nt + 1, nsave):
    filepath = simu_dir / 'solution' / f'ellipse_{n:0>7}.2D'
    with open(filepath, 'r') as infile:
        x, y = numpy.loadtxt(infile, unpack=True)
    z = numpy.zeros_like(x)
    filepath = simu_dir / 'solution' / f'ellipse_{n:0>7}.3D'
    with open(filepath, 'w') as outfile:
        numpy.savetxt(outfile, numpy.c_[x, y, z])
