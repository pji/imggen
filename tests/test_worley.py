"""
test_worley
~~~~~~~~~~~

Unit tests for the imggen.worley module.
"""
import pytest as pt
import numpy as np

import imggen.worley as w
from tests.common import mkhex


class TestWorley:
    # Tests for Worley initialization.
    def test_init_all_default(self):
        """Given only required parameters, :class:`Worley` should
        initialize the required attributes with the given values. It
        should then initialize the optional attributes with default
        values.
        """
        required = {
            'points': 10,
        }
        optional = {
            'volume': None,
            'origin': (0, 0, 0),
            'seed': None,
        }
        obj = w.Worley(**required)
        for attr in required:
            assert getattr(obj, attr) == required[attr]
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    def test_init_all_optional(self):
        """Given optional parameters, :class:`Worley` should
        initialize the given attributes with the given values.
        """
        required = {
            'points': 10,
        }
        optional = {
            'volume': (1, 3, 4),
            'origin': (4, 4, 4),
            'seed': 'spam',
        }
        obj = w.Worley(**required, **optional)
        for attr in required:
            assert getattr(obj, attr) == required[attr]
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    # Tests for fill.
    def test_fill(self):
        """Given origin, dimensions, and a color, :meth:`Worley.fill`
        should return a volume filled with a box of the origin,
        dimensions, and color given when the object was created.
        """
        obj = w.Worley(points=6, volume=None, seed='spam')
        result = obj.fill((3, 12, 8))
        assert (mkhex(result) == np.array([
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
        ], dtype=np.uint8)).all()


class TestOctaveWorley:
    # Tests for Worley initialization.
    def test_init_all_default(self):
        """Given only required parameters, :class:`OctaveWorley` should
        initialize the required attributes with the given values. It
        should then initialize the optional attributes with default
        values.
        """
        required = {}
        optional = {
            'octaves': 4,
            'persistence': 8,
            'amplitude': 8,
            'frequency': 2,
            'points': 10,
            'volume': None,
            'origin': (0, 0, 0),
            'seed': None,
        }
        obj = w.OctaveWorley(**required)
        for attr in required:
            assert getattr(obj, attr) == required[attr]
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    def test_init_all_optional(self):
        """Given optional parameters, :class:`OctaveWorley` should
        initialize the given attributes with the given values.
        """
        required = {}
        optional = {
            'octaves': 3,
            'persistence': 10,
            'amplitude': 9,
            'frequency': 4,
            'points': 8,
            'volume': (1, 3, 4),
            'origin': (4, 4, 4),
            'seed': 'spam',
        }
        obj = w.OctaveWorley(**required, **optional)
        for attr in required:
            assert getattr(obj, attr) == required[attr]
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    # Tests for fill.
    def test_fill(self):
        """Given origin, dimensions, and a color, :meth:`Worley.fill`
        should return a volume filled with a box of the origin,
        dimensions, and color given when the object was created.
        """
        obj = w.OctaveWorley(points=6, volume=None, seed='spam')
        result = obj.fill((1, 8, 8))
        assert (mkhex(result) == np.array([
            [
                [0x96, 0x18, 0xa0, 0x36, 0xca, 0xb9, 0xbd, 0x9e],
                [0x00, 0x00, 0x96, 0x30, 0x6c, 0x30, 0x51, 0x08],
                [0x00, 0x96, 0x58, 0x36, 0x22, 0x18, 0x4e, 0x00],
                [0x18, 0x1b, 0x5d, 0x26, 0x18, 0x00, 0x18, 0x4e],
                [0x99, 0x08, 0x4e, 0x51, 0x08, 0x00, 0x00, 0x08],
                [0x08, 0x00, 0x00, 0x4e, 0x4e, 0x00, 0x08, 0x1b],
                [0x0b, 0x96, 0x96, 0x51, 0x08, 0x00, 0x18, 0x9e],
                [0xa0, 0xd9, 0xae, 0x22, 0x0b, 0x18, 0x99, 0x12],
            ],
        ], dtype=np.uint8)).all()
