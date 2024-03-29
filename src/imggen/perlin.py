"""
perlin
~~~~~~

Image data sources that create Perlin noise.
"""
from typing import Sequence

import numpy as np
from numpy.typing import NDArray

from imggen import unitnoise as un
from imggen.imggen import ImgAry, Loc, Size, X, Y, Z


# Names available for import.
__all__ = ['OctavePerlin', 'Perlin',]


# Public class.
class Perlin(un.UnitNoise):
    """A class to generate Perlin noise.

    .. figure:: images/perlin.jpg
       :alt: A picture of an image created from the output of
            :class:`Perlin`.
       
       Output of :class:`Perlin`.

    :param unit: The number of pixels between vertices along an
        axis on the unit grid. The vertices are the locations where
        colors for the gradient are set. This is involved in setting
        the maximum size of noise that can be generated from
        the object.
    :param min: (Optional.) The minimum value of a vertex of the unit
        grid. This is involved in setting the maximum size of noise
        that can be generated from the object. Unless you have a very
        good reason, this is probably best left at the default.
    :param max: (Optional.) The maximum value of a vertex of the unit
        grid. This is involved in setting the maximum size of noise
        that can be generated from the object. Unless you have a very
        good reason, this is probably best left at the default.
    :param repeats: (Optional.) The number of times each value can
        appear on the unit grid. This is involved in setting the
        maximum size of noise that can be generated from the object.
        Unless you have a very good reason, this is probably best left
        at the default.
    :param seed: (Optional.) An int, bytes, or string used to seed
        therandom number generator used to generate the image data.
        If no value is passed, the RNG will not be seeded, so
        serialized versions of this source will not produce the
        same values. Note: strings that are passed to seed will
        be converted to UTF-8 bytes before being converted to
        integers for seeding.
    :return: :class:Perlin object.
    :rtype: imggen.perlin.Perlin
    """
    def __init__(
        self, unit: Sequence[int],
        min: int = 0x00,
        max: int = 0xff,
        repeats: int = 1,
        seed: un.Seed = None
    ) -> None:
        """Initialize an instance of UnitNoise."""
        super().__init__(unit, min, max, repeats, seed)

    # Public classes.
    def fill(
        self, size: Size,
        loc: Loc = (0, 0, 0)
    ) -> ImgAry:
        """Fill a volume with image data.

        :param size: The size of the volume of image data to generate.
        :param loc: (Optional.) How much to shift the starting point
            for the noise generation along each axis.
        :return: An :class:`numpy.ndarray` with image data.
        :rtype: numpy.ndarray
        """
        shape = self._calc_unit_grid_shape(size)
        whole, parts = self._map_unit_grid(size, loc)
        fades = 6 * parts ** 5 - 15 * parts ** 4 + 10 * parts ** 3
        grids = self._build_grids(whole, size, shape)
        for grid in grids:
            grids[grid] = self._grad(grid, grids[grid], parts)
        a = self._interp(grids, fades)
        return (a + 1) / 2

    # Private methods.
    def _build_grids(
        self, whole: np.ndarray,
        size: Sequence[float],
        shape: Sequence[int]
    ) -> dict[str, np.ndarray]:
        """Get the color for the eight vertices that surround each of
        the pixels.
        """
        grids = {}
        for key in self._hashes:
            grid_whole = whole.copy()
            for axis in range(self._axes):
                grid_whole[axis] += int(key[axis])

            a_grid = grid_whole[Z].astype(np.int64)
            for axis in (Y, X):
                a_grid = np.take(self._table, a_grid) + grid_whole[axis]

            grids[key] = a_grid
        return grids

    def _grad(self, loc_mask, grid, parts):
        """To be honest, I don't fully understand what this part of
        the Perlin noise algorithm is doing. It's called the
        gradient, so it must have something to do with how the
        level of noise changes between unit vertices. Beyond that
        I'm not sure.
        """
        z = parts[Z].copy()
        y = parts[Y].copy()
        x = parts[X].copy()
        if loc_mask[0] == '1':
            z -= 1
        if loc_mask[1] == '1':
            y -= 1
        if loc_mask[2] == '1':
            x -= 1

        m = grid & 0xf
        out = np.zeros_like(x)
        out[m == 0x0] = x[m == 0x0] + y[m == 0x0]
        out[m == 0x1] = -x[m == 0x1] + y[m == 0x1]
        out[m == 0x2] = x[m == 0x2] - y[m == 0x2]
        out[m == 0x3] = -x[m == 0x3] - y[m == 0x3]
        out[m == 0x4] = x[m == 0x4] + z[m == 0x4]
        out[m == 0x5] = -x[m == 0x5] + z[m == 0x5]
        out[m == 0x6] = x[m == 0x6] - z[m == 0x6]
        out[m == 0x7] = -x[m == 0x7] - z[m == 0x7]
        out[m == 0x8] = y[m == 0x8] + z[m == 0x8]
        out[m == 0x9] = -y[m == 0x9] + z[m == 0x9]
        out[m == 0xa] = y[m == 0xa] - z[m == 0xa]
        out[m == 0xb] = -y[m == 0xb] - z[m == 0xb]
        out[m == 0xc] = y[m == 0xc] + x[m == 0xc]
        out[m == 0xd] = -y[m == 0xd] + z[m == 0xd]
        out[m == 0xe] = y[m == 0xe] - x[m == 0xe]
        out[m == 0xf] = -y[m == 0xf] - z[m == 0xf]
        return out.astype(float)


# Octave unit noise classes.
defaults = un.OctaveNoiseDefaults(6, -4, 24, 4)
OctavePerlin = un.octave_noise_factory(Perlin, defaults)
