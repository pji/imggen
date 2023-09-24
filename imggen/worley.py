"""
worley
~~~~~~

Image data sources that create Worley noise.
"""
from typing import Optional, Sequence

import numpy as np
from numpy.typing import NDArray

from imggen.noise import Seed, Noise


# Public classes.
class Worley(Noise):
    """Fill a space with Worley noise.

    Worley noise is a type of cellular noise. The color value of each
    pixel within the space is determined by the distance from the pixel
    to the nearest of a set of randomly located points within the
    image. This creates structures within the noise that look like
    cells or pits.

    This implementation is heavily optimized from code found here:
    https://code.activestate.com/recipes/578459-worley-noise-generator/

    :param points: The number of cells in the image. A cell is a
        randomly placed point and the range of pixels that are
        closer to it than any other point.
    :param volume: (Optional.) The size of the volume that the points
        will be placed in. The default is for them to be evenly spread
        through the space generated during the fill.
    :param origin: (Optional.) The location of the upper-top-left
        corner of the volume that contains the points. This defaults
        to the upper-top-left corner of the space generated during the
        fill.
    :param seed: (Optional.) An int, bytes, or string used to seed
        therandom number generator used to generate the image data.
        If no value is passed, the RNG will not be seeded, so
        serialized versions of this source will not product the
        same values. Note: strings that are passed to seed will
        be converted to UTF-8 bytes before being converted to
        integers for seeding.
    :return: :class:Worley object.
    :rtype: imggen.worley.Worley
    """
    def __init__(
        self, points: int,
        volume: Optional[Sequence[int]] = None,
        origin: Sequence[int] = (0, 0, 0),
        seed: Seed = None
    ) -> None:
        self.points = points
        self.volume = volume
        self.origin = origin
        super().__init__(seed)

    def fill(
        self, size: Sequence[int],
        loc: Sequence[int] = (0, 0, 0)
    ) -> NDArray[np.float_]:
        """Return a space filled with noise."""
        a = np.zeros(size, dtype=float)
        volume_size = self.volume
        if volume_size is None:
            volume_size = size
        volume = np.array(volume_size, dtype=float)

        # Place the seeds in the overall volume of noise.
        seeds = self._rng.random((self.points, 3), dtype=float)
        seeds = np.around(seeds * (volume - 1)).astype(float)
        seeds += np.array(self.origin)

        # Map the distances to the points.
        indices = np.indices(size)
        max_dist = np.sqrt(sum(n ** 2 for n in size))
        dist = np.zeros(size, dtype=float)
        dist.fill(max_dist)
        for i in range(self.points):
            point = seeds[i]
            work = self._hypot(point, indices)
            dist[work < dist] = work[work < dist]

        act_max_dist = np.max(dist)
        a = dist / act_max_dist
        return a

    # Private methods.
    def _hypot(self, point: Sequence[int], indices: np.ndarray) -> np.ndarray:
        axis_dist = [p - i for p, i in zip(point, indices)]
        return np.sqrt(sum(d ** 2 for d in axis_dist))
