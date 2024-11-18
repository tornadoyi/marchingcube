from typing import Tuple
import math
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.widgets import Button, Slider
from tkinter.filedialog import askopenfilename
import numpy as np
from marchingcube import data
from marchingcube import mc

__all__ = [
    'Application'
]


class Application(object):

    _figure: plt.Figure
    _ax: Axes

    _bt_load: Button
    _bt_load_nrrd: Button
    _bt_load_math: Button
    _sld_isosurface: Slider

    _raw_data: np.ndarray
    _block_data: np.ndarray
    _data_value_range: Tuple[float, float]
    _isosurface_ratio: float

    def __init__(
        self,
        size: Tuple[int, int] = (10, 10),
        title: str = 'marching cubes',
    ) -> None:
        self._isosurface_ratio = 1
        self._sample_ratio = 0.5
        self._figure = plt.figure(title, figsize=size)
        self._ax = self._figure.add_subplot(projection='3d')

        # load button
        ax = self._figure.add_axes([0.1, 0.05, 0.09, 0.05])
        self._bt_load = Button(ax, 'Load Raw')
        self._bt_load.on_clicked(self._on_load_raw)

        # load nrrd
        ax = self._figure.add_axes([0.2, 0.05, 0.09, 0.05])
        self._bt_load_nrrd = Button(ax, 'Load Nrrd')
        self._bt_load_nrrd.on_clicked(self._on_load_nrrd)

        # load math
        ax = self._figure.add_axes([0.3, 0.05, 0.09, 0.05])
        self._bt_load_math = Button(ax, 'Load Math')
        self._bt_load_math.on_clicked(self._on_load_math)

        # generate
        ax = self._figure.add_axes([0.7, 0.05, 0.09, 0.05])
        self._bt_generate = Button(ax, 'Generate')
        self._bt_generate.on_clicked(self._on_generate)

        # isosurface slider
        ax = self._figure.add_axes([0.6, 0.9, 0.3, 0.03])
        self._sld_isosurface = Slider(
            ax,
            'Isosurface Ratio',
            valmin=0,
            valmax=1,
            valinit=self._isosurface_ratio,
        )
        self._sld_isosurface.on_changed(self._on_isosurface_changed)

        # sample slider
        ax = self._figure.add_axes([0.6, 0.85, 0.3, 0.03])
        self._sld_sample= Slider(
            ax,
            'Sample Ratio',
            valmin=0,
            valmax=1,
            valinit=self._sample_ratio,
        )
        self._sld_sample.on_changed(self._on_smaple_ratio_changed)

    def run(self):
        plt.show()

    def _on_load_raw(self, event):
        fpath = askopenfilename()
        if len(fpath) == 0:
            return
        self._process_raw_data(data.load_raw(fpath))
        self._render()

    def _on_load_nrrd(self, event):
        self._process_raw_data(data.load_random_nrrd())
        self._render()

    def _on_load_math(self, event):
        self._process_raw_data(data.load_random_math())
        self._render()

    def _on_isosurface_changed(self, value):
        if abs(self._isosurface_ratio - value) < 1e-3:
            return
        self._isosurface_ratio = value

    def _on_generate(self, event):
        self._process_raw_data(self._raw_data)
        self._render()

    def _on_smaple_ratio_changed(self, value):
        self._sample_ratio = value

    def _process_raw_data(self, raw_data: np.ndarray):
        self._raw_data = raw_data
        max_cells = int(self._sample_ratio * 100)
        print(f"max_cells: {max_cells} {self._sample_ratio}")
        self._block_data = mc.make_block(self._raw_data, max_cells=(max_cells, ) * 3)
        self._data_value_range = (
            self._block_data.min(), self._block_data.max())
        
    def _render(self):
        self._ax.clear()

        # calculate isosurface
        r = self._data_value_range
        isosurface = r[0] + (r[1] - r[0]) * self._isosurface_ratio
        isosurface = np.clip(isosurface, r[0]+1e-5, r[1]-1e-5)

        # marching cubes
        verts, faces = mc.marching_cubes(self._block_data, isosurface, verbose=False)
        self._ax.plot_trisurf(
            verts[:, 0], verts[:, 1], faces, verts[:, 2], cmap='Spectral', lw=1)
        
        # flush
        self._figure.canvas.draw()
        self._figure.canvas.flush_events()
