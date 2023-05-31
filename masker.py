#!/usr/bin/env python3
from pilatus import Pilatus, Gaps, SubModules
from ezplot import create_basic_plot
import numpy as np


class Mask(Pilatus):
    def __init__(self):
        self.pixel_matrix = Pilatus.Dimensions.pixel_matrix

    def mask_outer_edges(self):
        self.pixel_matrix[[0, -1], :] = 1
        self.pixel_matrix[:, [0, -1]] = 1

    def mask_gaps(self, pad=1):
        for xl, xu in Gaps.x_strips:
            self.pixel_matrix[:, xl-pad:xu+pad+1] = 1
        for yl, yu in Gaps.y_strips:
            self.pixel_matrix[yl-pad:yu+pad+1, :] = 1

    def mask_modules(self, pad=1):
        for x in SubModules.modulex_center_x:
            self.pixel_matrix[:, x-pad:x+pad+1] = 1
        for y in SubModules.modules_center_y:
            self.pixel_matrix[y-pad:y+pad+1, :] = 1

    def apply_mask(self, path_to_data: str):
        data = np.load(path_to_data)
        bool_mask = np.logical_or(self.pixel_matrix, data)
        self.pixel_matrix = bool_mask.astype(int)

    def plot_mask(self):
        xlabel = 'X_Pixel'
        ylabel = 'Y_Pixel'
        title = 'Mask'
        fig, ax = create_basic_plot(xlabel, ylabel, title, T=True)
        ax.imshow(self.pixel_matrix, origin='lower')
        return fig, ax
