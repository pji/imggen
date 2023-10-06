"""
common
~~~~~~

Common code used in multiple test modules
"""
import numpy as np


# Utility functions.
def mkhex(a):
    return (a * 0xff).astype(np.uint8)
