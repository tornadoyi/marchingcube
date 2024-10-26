import os
import random
import nrrd
import numpy as np
from . import mathdata


__all__ = [
    'load_random',
    'load',
]


CUR_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_nrrd(fpath: str) -> np.ndarray:
    readdata, header = nrrd.read(fpath)
    return readdata


FILE_EXT_LOADER = {
    '.nrrd': _load_nrrd
}


def load_random_nrrd() -> np.ndarray:
    data_files = [
        os.path.join(CUR_DIR, f)
        for f in os.listdir(CUR_DIR)
        if os.path.splitext(f)[-1] in FILE_EXT_LOADER
    ]

    index = random.randint(0, len(data_files)-1)
    fpath = data_files[index]
    return load(fpath)


def load_random_math() -> np.ndarray:
    data_fns = mathdata.all()
    index = random.randint(0, len(data_fns)-1)
    fn = getattr(mathdata, data_fns[index])
    return fn()


def load(fpath: str):
    ext = os.path.splitext(fpath)[-1]
    loader = FILE_EXT_LOADER.get(ext)
    if loader is None:
        raise KeyError(
            f"unsupported data file extension '{ext}', expected: {list(FILE_EXT_LOADER.keys())}")
    return loader(fpath)
