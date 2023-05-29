#!/usr/bin/python3
from dataclasses import dataclass
from typing import Tuple
import numpy as np


@dataclass
class Pilatus:
    x_pixels: int = 1475
    y_pixels: int = 1679
    pixel_size: float = 1.72e-4
    x_len: float = x_pixels * pixel_size
    y_len: float = y_pixels * pixel_size
    pixel_matrix = np.zeros((y_pixels, x_pixels))


@dataclass
class Gaps:
    FIRST_Y: int = 196
    LAST_Y: int = 1475
    Y_OFFSET: int = 212
    Y_POS = np.arange(FIRST_Y, LAST_Y, Y_OFFSET)
    Y_WIDTH: int = 16
    X_WIDTH: int = 6
    X_POS: Tuple = (488, 982)
    # bugs.python.org/issue3692
    y_strips = tuple((y, y + 6) for y in Y_POS)  # 6 = X_WIDTH
    x_strips = tuple((x, x + 16) for x in X_POS)  # 16 = Y_WIDTH


@dataclass
class SubModules:
    X_REPEAT: Tuple = (61, 128, 61, 128, 61)
    X_COUNT: Tuple = (7, 1, 6, 1, 6)
    Y_OFFSET: int = 98

    modulex_center_x = np.cumsum(np.repeat(X_REPEAT, X_COUNT))
    modules_center_y = np.concatenate(
        [[Y_OFFSET], np.array(Gaps.y_strips)[:, 0] + Y_OFFSET]

    )
