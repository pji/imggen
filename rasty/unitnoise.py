"""
unitnoise
~~~~~~~~~

Image data sources that create unit noise.
"""
from typing import Sequence

import numpy as np

from rasty.noise import Noise, Seed
from rasty.rasty import X, Y, Z
from rasty.utility import lerp


class UnitNoise(Noise):
    """Create image noise that is based on a unit grid."""
    hashes = [f'{n:>03b}'[::-1] for n in range(2 ** 3)]
    
    def __init__(self, unit: Sequence[int], 
                 min: int = 0x00,
                 max: int = 0xff,
                 repeats: int = 0,
                 seed: Seed = None) -> None:
        # Initialize public values.
        self.unit = unit
        self.min = min
        self.max = max
        self.repeats = repeats
        super().__init__(seed)
        
        # Initialize the randomized table.
        self._table = self._init_table()
    
    # Public methods.
    def fill(self, size: Sequence[int],
             location: Sequence[int] = (0, 0, 0)) -> np.ndarray:
        """Return a space filled with noise."""
        shape = []
        for axis in Z, Y, X:
            length = size[axis] // self.unit[axis]
            if size[axis] % self.unit[axis]:
                length += 1
            shape.append(length)
        
        # Map out the space.
        a = np.indices(size, float)
        for axis in X, Y, Z:
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

        # Get the color for the eight vertices that surround each of
        # the pixels.
        grids = self._build_grids(whole, size, shape)
        a = self._terp(grids, parts)
        return a / (self.max - self.min)

    # Private methods.
    def _build_grids(self, whole: np.ndarray, 
                     size: Sequence[float],
                     shape: Sequence[int]) -> dict[str, np.ndarray]:
        grids = {}
        for hash in self.hashes:
            hash_whole = whole.copy()
            a_hash = np.zeros(size)
            if hash[2] == '1':
                hash_whole[X] += 1
            if hash[1] == '1':
                hash_whole[Y] += 1
            if hash[0] == '1':
                hash_whole[Z] += 1
            a_hash = (hash_whole[Z] * shape[Y] * shape[X]
                      + hash_whole[Y] * shape[X]
                      + hash_whole[X])
            a_hash = np.take(self._table, a_hash)
            grids[hash] = a_hash
        return grids
    
    def _init_table(self) -> list[int]:
        """Create the table of randomized values for the unit grid."""
        table = []
        for repeat in range(self.repeats + 1):
            table.extend(list(range(self.min, self.max)))
        self._rng.shuffle(table)
        return table

    def _terp(self, grids: np.ndarray, parts: np.ndarray) -> np.ndarray:
        x1 = lerp(grids['000'], grids['001'], parts[X])
        x2 = lerp(grids['010'], grids['011'], parts[X])
        x3 = lerp(grids['100'], grids['101'], parts[X])
        x4 = lerp(grids['110'], grids['111'], parts[X])

        y1 = lerp(x1, x2, parts[Y])
        y2 = lerp(x3, x4, parts[Y])
        del x1, x2, x3, x4

        z = lerp(y1, y2, parts[Z])
        return z
        

if __name__ == '__main__':
    import rasty.utility as u
    kwargs = {
        'unit': (2, 2, 2),
        'min': 0x00,
        'max': 0xff,
        'seed': 'spam',
    }
    cls = UnitNoise
    size = (2, 8, 8)
    obj = cls(**kwargs)
    a = obj.fill(size)
    u.print_array(a)
