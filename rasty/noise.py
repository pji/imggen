"""
noise
~~~~~

Image data sources that contain a random element.
"""
from typing import Generator, Sequence, Union

import numpy as np
from numpy.random import default_rng

from rasty.sources import Source


# Public classes.
class Noise(Source):
    """Create continuous-uniformly distributed random noise with a
    seed value to allow the noise to be regenerated in a predictable
    way.

    :param seed: (Optional.) An int, bytes, or string used to seed
        therandom number generator used to generate the image data.
        If no value is passed, the RNG will not be seeded, so
        serialized versions of this source will not product the
        same values. Note: strings that are passed to seed will
        be converted to UTF-8 bytes before being converted to
        integers for seeding.
    :return: :class:Noise object.
    :rtype: rasty.noise.Noise
    """
    def __init__(self,
                 seed: Union[None, int, str, bytes] = None) -> None:
        """Initialize an instance of Noise."""
        # Store the seed for potential serialization.
        self.seed = seed
        
        # This seeds the random number generator. The code here is
        # maybe a bit opaque. Think about changing it in the future.
        self._rng = seed

    # Properties.
    @property
    def _rng(self) -> Generator:
        return self._Randomized__rng
    
    @_rng.setter
    def _rng(self, seed: Union[None, int, str, bytes]) -> None:
        # The seed value for numpy.default_rng cannot be a string.
        # You can't convert directly from string to integer, so
        # convert the string to bytes.
        if isinstance(seed, str):
            seed = bytes(seed, 'utf_8')
        
        # The seed value for numpy.default_rng needs to be an integer.
        if isinstance(seed, bytes):
            seed = int.from_bytes(seed, 'little')
        self._Randomized__rng = default_rng(seed)
    
    # Public methods.
    def fill(self, size: Sequence[int],
             loc: Sequence[int] = (0, 0, 0)) -> np.ndarray:
        # Random number generation is linear and unidirectional. In
        # order to give the illusion of their being a space to move
        # in, we define the location of the first number generated
        # as the origin of the space (so: [0, 0, 0]). We then will
        # make the negative locations in the space the reflection of
        # the positive spaces.
        new_loc = [abs(n) for n in loc]

        # To simulate positioning within a space, we need to burn
        # random numbers from the generator. This would be easy if
        # we were just generating single dimensional noise. Then
        # we'd only need to burn the first numbers from the generator.
        # Instead, we need to burn until with get to the first row,
        # then accept. Then we need to burn again until we get to
        # the second row, and so on. This implementation isn't very
        # memory efficient, but it should do the trick.
        new_size = [s + l for s, l in zip(size, new_loc)]
        a = self._rng.random(new_size)
        slices = tuple(slice(n, None) for n in new_loc)
        a = a[slices]
        return a
