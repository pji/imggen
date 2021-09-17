"""
utility
~~~~~~~

Utility functions for imggen.
"""
from typing import Any

import numpy as np


# Common types.
# The ArrayLike type is intended to match numpy's array-like
# descriptive type, which is anything that numpy.array can turn
# into a numpy.ndarray object. That is, ultimately, anything, but
# use of ArrayLike in the type hints is intended to communicate
# the data will be converted to an ndarray, which may have
# consequences.
ArrayLike = Any


# Debugging utilities.
def print_array(a: np.ndarray, depth: int = 0, color: bool = True) -> None:
    """Write the values of the given array to stdout."""
    if len(a.shape) > 1:
        print(' ' * (4 * depth) + '[')
        for i in range(a.shape[0]):
            print_array(a[i], depth + 1, color)
        print(' ' * (4 * depth) + '],')

    else:
        if a.dtype != np.uint8 and color:
            a = (a.copy() * 0xff).astype(np.uint8)
            tmp = '0x{:02x}'
        else:
            tmp = '{}'
        nums = [tmp.format(n) for n in a]
        print(' ' * (4 * depth) + '[' + ', '.join(nums) + '],')


# Interpolation utilities.
def lerp(a: ArrayLike, b: ArrayLike, x: ArrayLike) -> np.ndarray:
    """Perform a linear interpolation on the values of two arrays

    :param a: The "left" values.
    :param b: The "right" values.
    :param x: An array of how close the location of the final value
        should be to the "left" value.
    :return: A :class:ndarray object
    :rtype: numpy.ndarray

    Usage::

        >>> import numpy as np
        >>>
        >>> a = np.array([1, 2, 3])
        >>> b = np.array([3, 4, 5])
        >>> x = np.array([.5, .5, .5])
        >>> lerp(a, b, x)
        array([2., 3., 4.])
    """
    a = np.array(a.copy(), dtype=float)
    b = np.array(b.copy(), dtype=float)
    x = np.array(x.copy(), dtype=float)
    return a * (1 - x) + b * x
