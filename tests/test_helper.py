import math
import numpy as np

from math import pi, ceil


def random_sphere_points(n_points, dim):
    assert dim == 3

    # @see http://en.wikipedia.org/wiki/Spherical_coordinate_system
    r = 1
    theta = np.random.rand(n_points) * 2 * math.pi
    phi = np.random.rand(n_points) * 2 * math.pi

    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    return np.column_stack((x, y, z))


def sphere_points(n, dim, r=1):
    """

    :param n: At least n points will be generated.
    :param dim:
    """

    # Calculate the (dim-1)'th root of n, which is the number of iterations per
    # dimension.
    n_dim = ceil(n ** (1. / (dim - 1)))
    n_total = n_dim ** (dim - 1)

    # The first dim -1 angles range from [0, pi] and the last from [0, 2pi[.
    # @see http://en.wikipedia.org/wiki/N-sphere
    angspace = np.zeros((dim - 1, n_dim), dtype=np.float64)
    angspace[:-1] = np.linspace(0, pi, n_dim)
    angspace[-1] = np.linspace(0, 2 * pi, n_dim + 1)[:-1]

    # Create an array of n - 1 angles for each point.
    # There are no two points with the same angles.
    # TODO: Problem in regard to f.ex.h sin 0 =~= pi
    ang = np.zeros((dim - 1, n_total), dtype=np.float64)
    for i in range(n_total):
        for j in range(dim - 1):
            k = (i // (n_dim ** j)) % n_dim
            ang[j][i] = angspace[j][k]

    # The spherical coordinates will be calculated as shown in
    # @see http://en.wikipedia.org/wiki/N-sphere#Spherical_coordinates
    points = np.zeros((n_total, dim))
    _points = points.T

    _points[0] = r * np.cos(ang[0])
    sin_cum = r * np.sin(ang[0])
    for i in range(1, dim - 1):
        _points[i] = sin_cum * np.cos(ang[i])
        sin_cum *= np.sin(ang[i])

    if dim > 2:
        _points[-1] = sin_cum * np.sin(ang[-1])
    else:
        _points[-1] = sin_cum

    return points
