"""
unitnoise
~~~~~~~~~

Image data sources that create unit noise.
"""
from typing import NamedTuple, Sequence

import numpy as np
from numpy.typing import NDArray

from imggen.imggen import ImgAry, Loc, Size, Source, X, Y, Z
from imggen.noise import Noise, Seed
from imggen.utility import lerp


# Public classes.
class UnitNoise(Noise):
    """Create image noise that is based on a unit grid.

    :param unit: The number of pixels between vertices along an
        axis on the unit grid. The vertices are the locations where
        colors for the gradient are set. This is involved in setting
        the maximum size of noise that can be generated from
        the object.
    :param min: (Optional.) The minimum value of a vertex of the unit
        grid. This is involved in setting the maximum size of noise
        that can be generated from the object.
    :param max: (Optional.) The maximum value of a vertex of the unit
        grid. This is involved in setting the maximum size of noise
        that can be generated from the object.
    :param repeats: (Optional.) The number of times each value can
        appear on the unit grid. This is involved in setting the
        maximum size of noise that can be generated from the object.
    :param seed: (Optional.) An int, bytes, or string used to seed
        therandom number generator used to generate the image data.
        If no value is passed, the RNG will not be seeded, so
        serialized versions of this source will not produce the
        same values. Note: strings that are passed to seed will
        be converted to UTF-8 bytes before being converted to
        integers for seeding.
    """
    # The number of dimensions the noise occurs in.
    _axes = 3

    def __init__(
        self, unit: Sequence[int],
        min: int = 0x00,
        max: int = 0xff,
        repeats: int = 0,
        seed: Seed = None
    ) -> None:
        """Initialize an instance of UnitNoise."""
        # Initialize public values.
        self.unit = unit
        self.min = min
        self.max = max
        self.repeats = repeats
        super().__init__(seed)

        # Initialize the randomized table.
        self._table = self._init_table()

        # Prime the names of the grids used for interpolation.
        tmp = '{:>0' + str(self._axes) + 'b}'
        self._hashes = [tmp.format(n) for n in range(2 ** self._axes)]

    # Public methods.
    def fill(
        self, size: Size,
        location: Loc = (0, 0, 0)
    ) -> ImgAry:
        """Fill a volume with image data.

        :param size: The size of the volume of image data to generate.
        :param loc: (Optional.) How much to shift the starting point
            for the noise generation along each axis.
        :return: An :class:`numpy.ndarray` with image data.
        :rtype: numpy.ndarray
        """
        shape = self._calc_unit_grid_shape(size)
        whole, parts = self._map_unit_grid(size, location)
        grids = self._build_grids(whole, size, shape)
        a = self._interp(grids, parts)
        return a / (self.max - self.min)

    # Private methods.
    def _build_grids(
        self, whole: NDArray[np.int_],
        size: Sequence[int],
        shape: Sequence[int]
    ) -> dict[str, NDArray[np.int64]]:
        """Get the color for the eight vertices that surround each of
        the pixels.
        """
        grids = {}
        for key in self._hashes:
            grid_whole = whole.copy()
            a_grid = np.zeros(size, dtype=np.int64)
            for axis in range(self._axes):
                grid_whole[axis] += int(key[axis])

            for axis in range(self._axes):
                remaining_axes = range(self._axes)[axis + 1:]
                axis_incr = 1
                for r_axis in remaining_axes:
                    axis_incr *= shape[r_axis]
                a_grid += grid_whole[axis] * axis_incr
                a_grid %= len(self._table)

            a_grid = np.take(self._table, a_grid)
            grids[key] = a_grid
        return grids

    def _calc_unit_grid_shape(self, size: Sequence[int]):
        """Determine the shape of the unit grid."""
        shape = []
        for axis in range(self._axes):
            # Double inverse floor is ceiling division.
            length = -(-size[axis] // self.unit[axis])
            length = int(length)
            shape.append(length)

        return shape

    def _init_table(self) -> list[int]:
        """Create the table of randomized values for the unit grid."""
        table = []
        for repeat in range(self.repeats + 1):
            table.extend(list(range(self.min, self.max)))
        self._rng.shuffle(table)
        return table

    def _map_unit_grid(
        self, size: Sequence[int],
        location: Sequence[int]
    ) -> tuple[NDArray[np.int_], NDArray[np.float_]]:
        """Map the image data to the unit grid."""
        # Map out the space.
        a = np.indices(size, float)
        for axis in range(self._axes):
            a[axis] += location[axis]

            # Split the space up into units.
            a[axis] = a[axis] / self.unit[axis]
            a[axis] %= 255

        # The unit distances are split. The unit values are needed
        # to set the color value of each vertex within the volume.
        # The parts value is needed to interpolate the noise value
        # at each pixel.
        whole = (a // 1).astype(int)
        parts = a - whole
        return whole, parts

    def _interp(
        self, grids: dict[str, NDArray[np.int64]],
        parts: NDArray[np.float_]
    ) -> NDArray[np.float_]:
        """Interpolate the values of each pixel of image data."""
        if len(grids) > 2:
            new_grids = {}
            evens = [k for k in grids if k.endswith('0')]
            odds = [k for k in grids if k.endswith('1')]
            for even, odd in zip(evens, odds):
                new_key = even[:-1]
                axis = len(new_key)
                new_grids[new_key] = lerp(grids[even], grids[odd], parts[axis])
            return self._interp(new_grids, parts)

        return lerp(grids['0'], grids['1'], parts[Z])


class Curtains(UnitNoise):
    """Unit noise that creates vertical lines, like curtains."""
    # The number of dimensions the noise occurs in.
    _axes = 2

    # Public methods.
    def fill(self, size: Sequence[int],
             loc: Sequence[int] = (0, 0, 0)) -> np.ndarray:
        """Return a space filled with noise."""
        noise_size = (size[Z], size[X])
        noise_loc = (loc[Z], loc[X])
        a = super().fill(noise_size, noise_loc)
        return np.tile(a[:, np.newaxis, ...], (1, size[Y], 1))


class CosineCurtains(Curtains):
    """Unit noise that creates vertical lines with a cosine-based ease
    on the color change between grid points, making them appear to
    flow more like curtains.
    """
    # Private methods.
    def _map_unit_grid(
        self, size: Sequence[int],
        location: Sequence[int]
    ) -> tuple[NDArray[np.int_], NDArray[np.float_]]:
        """Map the image data to the unit grid."""
        whole, parts = super()._map_unit_grid(size, location)
        parts = (1 - np.cos(parts * np.pi)) / 2
        return whole, parts


# Factories.
class OctaveNoiseDefaults(NamedTuple):
    octaves: int = 4
    persistence: float = 8
    amplitude: float = 8
    frequency: float = 2
    unit: Sequence[int] = (1024, 1024, 1024)
    min: int = 0x00
    max: int = 0xff
    repeats: int = 1
    seed: Seed = None


def octave_noise_factory(
    source: type[UnitNoise],
    defaults: OctaveNoiseDefaults
) -> type:
    class OctaveNoise(Source):
        source: type[UnitNoise]

        def __init__(
            self, octaves: int = defaults.octaves,
            persistence: float = defaults.persistence,
            amplitude: float = defaults.amplitude,
            frequency: float = defaults.frequency,
            unit: Sequence[int] = defaults.unit,
            min: int = defaults.min,
            max: int = defaults.max,
            repeats: int = defaults.repeats,
            seed: Seed = defaults.seed
        ) -> None:
            self.octaves = octaves
            self.persistence = persistence
            self.amplitude = amplitude
            self.frequency = frequency
            self.unit = unit
            self.min = min
            self.max = max
            self.repeats = repeats
            self.seed = seed

        def fill(
            self, size: Sequence[int],
            loc: Sequence[int] = (0, 0, 0)
        ) -> NDArray[np.float_]:
            a = np.zeros(tuple(size), dtype=float)
            max_value = 0.0
            for i in range(self.octaves):
                amp = self.amplitude + (self.persistence * i)
                freq = self.frequency * 2 ** i
                unit = [n / freq for n in self.unit]
                octave = self.source(
                    unit=tuple(unit),
                    min=self.min,
                    max=self.max,
                    repeats=self.repeats,
                    seed=self.seed
                )
                a += octave.fill(size, loc) * amp
                max_value += amp
            a /= max_value
            return a

    cls = OctaveNoise
    cls.source = source
    return cls


# Octave unit noise classes.
defaults = OctaveNoiseDefaults()
OctaveCosineCurtains = octave_noise_factory(CosineCurtains, defaults)
OctaveCurtains = octave_noise_factory(Curtains, defaults)
OctaveUnitNoise = octave_noise_factory(UnitNoise, defaults)
