"""
Creates a YAML file with info about the structured Cartesian mesh that will be
parsed by PetIBM.

Creates a 2D structured Cartesian grid.
"""

import sys
import pathlib


root_dir = pathlib.Path(__file__).absolute().parents[3]
module_dir = root_dir / 'src/python'
if module_dir not in sys.path:
  sys.path.insert(0, str(module_dir))
from cartesianmesh import CartesianStructuredMesh


# Info about the 2D structured Cartesian grid.
width = 0.025  # minimum grid spacing in the x- and y- directions
ratio = 1.05  # stretching ratio
info = [{'direction': 'x', 'start': -15.0,
         'subDomains': [{'end': -2.0,
                         'width': width,
                         'stretchRatio': ratio,
                         'reverse': True,
                         'precision': 2},
                        {'end': 2.0,
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': 15.0,
                         'width': width,
                         'stretchRatio': ratio,
                         'precision': 2}]},
        {'direction': 'y', 'start': -15.0,
         'subDomains': [{'end': -3.0,
                         'width': width,
                         'stretchRatio': ratio,
                         'reverse': True,
                         'precision': 2},
                        {'end': 1.0,
                         'width': width,
                         'stretchRatio': 1.0},
                        {'end': 15.0,
                         'width': width,
                         'stretchRatio': ratio,
                         'precision': 2}]}]

mesh = CartesianStructuredMesh()
mesh.create(info, mode='cuibm')
mesh.print_parameters()
mesh.write_yaml_file('mesh.yaml')
