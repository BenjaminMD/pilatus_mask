#!/usr/bin/python3
import matplotlib.pyplot as plt
from pilatus import Pilatus, Gaps, SubModules
from ezplot import create_basic_plot
import numpy as np


class Mask(Pilatus):
    def mask_outer_edges(self):
        self.pixel_matrix[[0, -1], :] = 1
        self.pixel_matrix[:, [0, -1]] = 1

    def mask_gaps(self, overlap=1):
        for xl, xu in Gaps.x_strips:
            self.pixel_matrix[:, xl - overlap:xu + overlap + 1] = 1
        for yl, yu in Gaps.y_strips:
            self.pixel_matrix[yl - overlap:yu + overlap + 1, :] = 1

    def mask_modules(self, overlap=1):
        for x in SubModules.modulex_center_x:
            self.pixel_matrix[:, x - overlap:x + overlap + 1] = 1
        for y in SubModules.modules_center_y:
            self.pixel_matrix[y - overlap:y + overlap + 1, :] = 1

    def apply_mask(self, path_to_data: str):
        data = np.load(path_to_data)
        self.pixel_matrix = np.logical_or(self.pixel_matrix, data).astype(int)

    def plot_mask(self):
        fig, ax = create_basic_plot('X_Pixel', 'Y_Pixel', 'Mask', T=True)
        ax.imshow(self.pixel_matrix, origin='lower')
        return fig, ax



