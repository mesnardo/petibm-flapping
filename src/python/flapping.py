import pathlib
import numpy


def get_root_dir():
    root_dir = pathlib.Path(__file__).absolute().parents[2]
    return root_dir


def get_data_dir():
    root_dir = get_root_dir()
    data_dir = root_dir / 'data'
    return data_dir


def rotate(x, y, center=(0.0, 0.0), angle=0.0):
    """
    Applies a rotation around a center to given coordinates.

    Parameters
    ----------
    x: numpy.ndarray of floats
        The x-coordinates to rotate.
    y: numpy.ndarray of floats
        The y-coordinates to rotate.
    center: 2-tuple of floats, optional
        The center of rotation;
        default: (0.0, 0.0).
    angle: float, optional
        The angle of rotation in radians;
        default: 0.0.

    Returns
    -------
    x_new: numpy.ndarray of floats
        The rotated x-coordinates.
    y_new: numpy.ndarray of floats
        The rotated y-coordinates.
    """
    xc, yc = center
    x_new = xc + (x - xc) * numpy.cos(angle) - (y - yc) * numpy.sin(angle)
    y_new = yc + (x - xc) * numpy.sin(angle) + (y - yc) * numpy.cos(angle)
    return x_new, y_new


class Flapping(object):
    def __init__(self):
        self.Re = 75.0  # Reynolds number
        self.rho = 1.0  # density
        self.c = 1.0  # chord-length
        self.r = 0.10  # thickness-to-chord ratio
        self.A0 = 2.8 * self.c  # stroke amplitude
        self.f = 0.25  # flapping frequency
        self.Umax = self.A0 * numpy.pi * self.f  # max translational velocity
        self.alpha0 = numpy.pi / 2  # initial angle of attack
        self.beta = numpy.pi / 4  # amplitude of the pitching
        self.phi = 0.0  # phase difference between translation and rotation

    def orientation_angle(self, t):
        w = 2 * numpy.pi * self.f
        alpha = self.alpha0 + self.beta * numpy.sin(w * t + self.phi)
        return alpha

    def displacement(self, t):
        w = 2 * numpy.pi * self.f
        xd = self.A0 / 2 * numpy.cos(w * t)
        yd = 0.0
        return xd, yd

    def position(self, t, x0, y0):
        xd, yd = self.displacement(t)
        alpha = self.orientation_angle(t)
        x, y = x0 + xd, y0 + yd
        x, y = rotate(x, y, center=(xd, yd), angle=alpha)
        return x, y

    def translational_velocity(self, t):
        w = 2 * numpy.pi * self.f
        ux = -self.Umax * numpy.sin(w * t)
        uy = 0.0 if isinstance(t, float) else numpy.zeros_like(t)
        return ux, uy

    def angular_velocity(self, t):
        w = 2 * numpy.pi * self.f
        omega = w * self.beta * numpy.cos(w * t + self.phi)
        return omega

    def velocity(self, t, x, y, xc, yc):
        U0, V0 = self.translational_velocity(t)
        W0 = self.angular_velocity(t)
        ux = U0 - W0 * (y - yc)
        uy = V0 + W0 * (x - xc)
        return ux, uy

    def quasi_steady_coefficients(self, t):
        alpha = self.orientation_angle(t)
        U0, _ = self.translational_velocity(t)
        if isinstance(t, float):
            alpha = numpy.pi - alpha if U0 <= 0.0 else alpha
        else:
            mask = numpy.where(U0 <= 0.0)
            alpha[mask] = numpy.pi - alpha[mask]
        CD = 1.4 - numpy.cos(2 * alpha)
        CL = 1.2 * numpy.sin(2 * alpha)
        return CD, CL

    def quasi_steady_forces(self, t, x, y, xc, yc, rho=1.0):
        CD, CL = self.quasi_steady_coefficients(t)
        ux, uy = self.velocity(t, x, y, xc, yc)
        u = numpy.sqrt(ux**2 + uy**2)
        D = 0.5 * rho * u**2 * CD
        L = 0.5 * rho * u**2 * CL
        return D, L

    def get_CD_CL(self, filepath, bodypath):
        data = {}
        t, fx, fy = read_petibm_forces(filepath)
        # Non-dimensionalize time by the period.
        t_nodim = self.f * t
        # Reverse sign of force in x-direction when the body moving
        # in the positive x-direction.
        U0, _ = self.translational_velocity(t)
        fx *= -U0 / numpy.abs(U0)
        # Normalize the forces by the maximum quasi-steady force on the wing.
        D, L = [], []
        with open(bodypath, 'r') as infile:
            x0 = numpy.loadtxt(infile, skiprows=1, usecols=0, unpack=True)
            y0 = numpy.zeros_like(x0)
        for ti in t:
            alpha = self.orientation_angle(ti)
            x, y = rotate(x0, y0, center=(0.0, 0.0), angle=alpha)
            Di, Li = self.quasi_steady_forces(ti, x, y, 0.0, 0.0, rho=1.0)
            D.append(numpy.max(Di))
            L.append(numpy.max(Li))
        D, L = numpy.array(D), numpy.array(L)
        data['CD'] = [t_nodim, fx / numpy.max(D)]
        data['CL'] = [t_nodim, fy / numpy.max(L)]
        return data


def get_CD_CL(label, *args):
    if label == 'petibm':
        return Flapping().get_CD_CL(*args)
    elif label == 'Li et al. (2015)':
        return get_CD_CL_li_et_al_2015()
    elif label == 'Wang et al. (2004)':
        return get_CD_CL_wang_et_al_2004()
    elif label == 'Eldredge (2007)':
        return get_CD_CL_eldredge_2007()
    else:
        print(f'Label "{label}" is unknown label.')
    return


def get_CD_CL_li_et_al_2015():
    data = {}
    data_dir = get_data_dir()
    filepath = data_dir / 'CD_current.dat'
    with open(filepath, 'r') as infile:
        data['CD'] = numpy.loadtxt(infile, unpack=True)
    filepath = data_dir / 'CL_current.dat'
    with open(filepath, 'r') as infile:
        data['CL'] = numpy.loadtxt(infile, unpack=True)
    return data


def get_CD_CL_wang_et_al_2004():
    data = {}
    data_dir = get_data_dir()
    filepath = data_dir / 'CD_EXP.dat'
    with open(filepath, 'r') as infile:
        data['CD'] = numpy.loadtxt(infile, unpack=True)
    filepath = data_dir / 'CL_EXP.dat'
    with open(filepath, 'r') as infile:
        data['CL'] = numpy.loadtxt(infile, unpack=True)
    return data


def get_CD_CL_eldredge_2007():
    data = {}
    data_dir = get_data_dir()
    filepath = data_dir / 'CD_VVPM.dat'
    with open(filepath, 'r') as infile:
        data['CD'] = numpy.loadtxt(infile, unpack=True)
    filepath = data_dir / 'CL_VVPM.dat'
    with open(filepath, 'r') as infile:
        data['CL'] = numpy.loadtxt(infile, unpack=True)
    return data


def read_petibm_forces(filepath):
    with open(filepath, 'r') as infile:
        t, fx, fy = numpy.loadtxt(infile, unpack=True)
    return t, fx, fy
