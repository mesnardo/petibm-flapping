"""
Plots the history of the force coefficients and compare with results
published in Li et al. (2015).

Li, C., Dong, H., & Liu, G. (2015).
Effects of a dynamic trailing-edge flap on the aerodynamic performance
and flow structures in hovering flight.
Journal of Fluids and Structures, 58, 49-65.
"""

import sys
import pathlib
from matplotlib import pyplot


root_dir = pathlib.Path(__file__).absolute().parents[3]
module_dir = root_dir / 'src'/ 'python'
if module_dir not in sys.path:
    sys.path.insert(0, str(module_dir))
import flapping


data = {}

# Read the computational data from the present simulation.
key = 'PetIBM'
simu_dir = pathlib.Path(__file__).absolute().parents[1]
filepath = simu_dir / 'forces-0.txt'
bodypath = simu_dir / 'ellipse.body'
data[key] = flapping.get_CD_CL('petibm', filepath, bodypath)
data[key]['kwargs'] = {'color': 'C0', 'linestyle': '-', 'linewidth': 1,
                       'zorder': 4}

# Read the computational data from Li et al. (2015).
key = 'Li et al. (2015)'
data[key] = flapping.get_CD_CL(key)
data[key]['kwargs'] = {'color': 'C1', 'linestyle': '-', 'linewidth': 1,
                       'zorder': 3}

# Read the experimental data from Wang et al. (2004).
# The data were digitized Li and co-workers from Wang et al. (2004).
key = 'Wang et al. (2004)'
data[key] = flapping.get_CD_CL(key)
data[key]['kwargs'] = {'color': 'C2', 'linestyle': '--', 'linewidth': 1,
                       'zorder': 2}

# Read the computational data from Eldredge (2007).
# The data were digitized Li and co-workers from Eldredge (2007).
key = 'Eldredge (2007)'
data[key] = flapping.get_CD_CL(key)
data[key]['kwargs'] = {'color': 'black', 'linestyle': '--', 'linewidth': 1,
                       'zorder': 1}

# Set the type and size of the font to use in Matplotlib figures.
pyplot.rc('font', family='serif', size=16)

# Plot the lift and drag coefficients.
fig, ax = pyplot.subplots(nrows=2, figsize=(8.0, 6.0), sharex=True)
ax[0].set_ylabel('$C_L$')
ax[0].grid()
for label, subdata in data.items():
    ax[0].plot(*subdata['CL'], label=label, **subdata['kwargs'])
ax[0].set_ylim(-1.0, 2.0)
ax[1].set_xlabel('$t / T$')
ax[1].set_ylabel('$C_D$')
ax[1].grid()
for label, subdata in data.items():
    ax[1].plot(*subdata['CD'], label=label, **subdata['kwargs'])
ax[1].set_xlim(0.0, 4.0)
ax[1].set_ylim(-1.5, 2.0)
handles, labels = ax[1].get_legend_handles_labels()
fig.legend(handles, labels, prop={'size': 10},
           ncol=2, loc='center', frameon=False, bbox_to_anchor=(0.50, 0.54))
fig.tight_layout()

# Save the figure.
fig_dir = simu_dir / 'figures'
fig_dir.mkdir(parents=True, exist_ok=True)
filepath = fig_dir / 'forceCoefficients.png'
fig.savefig(str(filepath), dpi=300)

pyplot.show()
