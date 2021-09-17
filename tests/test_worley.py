"""
test_worley
~~~~~~~~~~~

Unit tests for the imggen.worley module.
"""
import numpy as np

import imggen.worley as w
from tests.common import SourceTestCase


# Test cases.
class WorleyTestCase(SourceTestCase):
    def test_fill(self):
        """Given a volume of image data to fill, Worley.fill should
        return that volume filled with Perlin noise.
        """
        # Expected value.
        exp = np.array([
            [
                [0x39, 0x28, 0x39, 0x5a, 0x7f, 0xa6, 0xcd, 0xf5],
                [0x28, 0x00, 0x28, 0x50, 0x78, 0xa1, 0xc9, 0xe7],
                [0x00, 0x28, 0x39, 0x5a, 0x7f, 0xa6, 0xb8, 0xc5],
                [0x28, 0x39, 0x5a, 0x72, 0x91, 0x91, 0x96, 0xa6],
                [0x39, 0x45, 0x62, 0x85, 0x78, 0x72, 0x78, 0x8b],
                [0x5a, 0x62, 0x78, 0x78, 0x62, 0x5a, 0x62, 0x78],
                [0x7f, 0x85, 0x85, 0x62, 0x45, 0x39, 0x45, 0x62],
                [0xa6, 0xa6, 0x7f, 0x5a, 0x39, 0x28, 0x39, 0x5a],
                [0xcd, 0xab, 0x85, 0x62, 0x45, 0x39, 0x45, 0x62],
                [0xd1, 0xab, 0x85, 0x62, 0x45, 0x39, 0x45, 0x62],
                [0xcd, 0xa6, 0x7f, 0x5a, 0x39, 0x28, 0x39, 0x5a],
                [0xd1, 0xab, 0x85, 0x62, 0x45, 0x39, 0x45, 0x62],
            ],
            [
                [0x45, 0x39, 0x45, 0x62, 0x85, 0xab, 0xd1, 0xf8],
                [0x39, 0x28, 0x39, 0x5a, 0x7f, 0xa6, 0xcd, 0xdc],
                [0x28, 0x39, 0x45, 0x62, 0x85, 0xa6, 0xab, 0xb8],
                [0x00, 0x28, 0x50, 0x78, 0x85, 0x7f, 0x85, 0x96],
                [0x28, 0x39, 0x5a, 0x78, 0x62, 0x5a, 0x62, 0x78],
                [0x50, 0x5a, 0x72, 0x62, 0x45, 0x39, 0x45, 0x62],
                [0x78, 0x7f, 0x7f, 0x5a, 0x39, 0x28, 0x39, 0x5a],
                [0xa1, 0xa1, 0x78, 0x50, 0x28, 0x00, 0x28, 0x50],
                [0xc9, 0xa6, 0x7f, 0x5a, 0x39, 0x28, 0x39, 0x5a],
                [0xcd, 0xa6, 0x7f, 0x5a, 0x39, 0x28, 0x39, 0x5a],
                [0xc9, 0xa1, 0x78, 0x50, 0x28, 0x00, 0x28, 0x50],
                [0xcd, 0xa6, 0x7f, 0x5a, 0x39, 0x28, 0x39, 0x5a],
            ],
            [
                [0x62, 0x5a, 0x62, 0x78, 0x96, 0xb8, 0xdc, 0xff],
                [0x5a, 0x50, 0x5a, 0x72, 0x91, 0xb4, 0xcd, 0xd9],
                [0x39, 0x45, 0x62, 0x78, 0x96, 0xa1, 0xa6, 0xb4],
                [0x28, 0x39, 0x5a, 0x7f, 0x7f, 0x78, 0x7f, 0x91],
                [0x39, 0x45, 0x62, 0x72, 0x5a, 0x50, 0x5a, 0x72],
                [0x5a, 0x62, 0x78, 0x5a, 0x39, 0x28, 0x39, 0x5a],
                [0x7f, 0x85, 0x78, 0x50, 0x28, 0x00, 0x28, 0x50],
                [0xa6, 0xa6, 0x7f, 0x5a, 0x39, 0x28, 0x39, 0x5a],
                [0xcd, 0xab, 0x85, 0x62, 0x45, 0x39, 0x45, 0x62],
                [0xd1, 0xab, 0x85, 0x62, 0x45, 0x39, 0x45, 0x62],
                [0xcd, 0xa6, 0x7f, 0x5a, 0x39, 0x28, 0x39, 0x5a],
                [0xd1, 0xab, 0x85, 0x62, 0x45, 0x39, 0x45, 0x62],
            ],
        ], dtype=np.uint8)

        # Test data and state.
        kwargs = {
            'points': 6,
            'volume': None,
            'origin': (0, 0, 0),
            'seed': 'spam',
        }
        cls = w.Worley

        # Run test and determine result.
        self.fill_test(exp, cls, kwargs)
