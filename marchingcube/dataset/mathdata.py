import numpy as np
from skimage import draw


__all__ = [
    'cos_sphere',
    'ellipsoid'
]


def all():
    return __all__


def cos_sphere(n=30):
    nj = complex(n)
    x, y, z = np.pi * np.mgrid[-1:1:nj, -1:1:nj, -1:1:nj]
    return np.cos(x) + np.cos(y) + np.cos(z)


def ellipsoid():
    ellip_base = draw.ellipsoid(6, 10, 16, levelset=True)
    return np.concatenate((ellip_base[:-1, ...], ellip_base[2:, ...]), axis=0)