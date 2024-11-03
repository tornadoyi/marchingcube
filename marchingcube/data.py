import os
import random
import nrrd
import numpy as np
import json
from skimage import draw


__all__ = [
    'load_random',
    'load',
]


def cos_sphere(n=30):
    nj = complex(n)
    x, y, z = np.pi * np.mgrid[-1:1:nj, -1:1:nj, -1:1:nj]
    return np.cos(x) + np.cos(y) + np.cos(z)


def ellipsoid():
    ellip_base = draw.ellipsoid(6, 10, 16, levelset=True)
    return np.concatenate((ellip_base[:-1, ...], ellip_base[2:, ...]), axis=0)


def _load_nrrd(fpath: str) -> np.ndarray:
    readdata, header = nrrd.read(fpath)
    return readdata


FILE_EXT_LOADERS = {
    '.nrrd': _load_nrrd
}

MATH_LOADERS = [
    cos_sphere,
    ellipsoid,
]


def load_random_nrrd() -> np.ndarray:
    dataset_path = os.environ['DATASET_PATH']
    data_files = [
        os.path.join(dataset_path, f)
        for f in os.listdir(dataset_path)
        if os.path.splitext(f)[-1] in FILE_EXT_LOADERS
    ]

    index = random.randint(0, len(data_files)-1)
    fpath = data_files[index]
    return load(fpath)


def load_random_math() -> np.ndarray:
    data_fns = MATH_LOADERS
    index = random.randint(0, len(data_fns)-1)
    fn = MATH_LOADERS[index]
    return fn()


_SCALAR_TYPES = {
    'unsigned_short': np.uint16,
    'short': np.int16,
    'unsigned_char': np.uint8,
    'char': np.int8,
}


def load_raw(fpath: str) -> np.ndarray:
    meta_fpath = os.path.splitext(fpath)[0] + '.json'
    if not os.path.isfile(meta_fpath):
        raise Exception(f"no such meta file {meta_fpath}")

    # meta
    with open(meta_fpath, 'r') as f:
        metadata = json.load(f)

    dimensions = metadata['dimensions']
    spacing = metadata['spacing']
    scalar_type = metadata['scalar_type']

    np_dtype = _SCALAR_TYPES.get(scalar_type)
    if np_dtype is None:
        raise ValueError(f"invalid scalar type {scalar_type}")

    # load raw
    raw_data = np.fromfile(fpath, dtype=np_dtype)
    return raw_data.reshape(dimensions[2], dimensions[1], dimensions[0])


def load(fpath: str):
    ext = os.path.splitext(fpath)[-1]
    loader = FILE_EXT_LOADERS.get(ext)
    if loader is None:
        raise KeyError(
            f"unsupported data file extension '{ext}', expected: {list(FILE_EXT_LOADERS.keys())}")
    return loader(fpath)
