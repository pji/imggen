"""
test_unitnoise
~~~~~~~~~~~~~~

Unit tests for the imggen.unitnoise module.
"""
import numpy as np
import pytest as pt

from imggen import unitnoise as un
from tests.common import mkhex


# Tests for base UnitNoise.
class TestUnitNoise:
    def test_init_all_default(self):
        """Given only required parameters, :class:`UnitNoise` should
        initialize the required attributes with the given values. It
        should then initialize the optional attributes with default
        values.
        """
        required = {'unit': (4, 4, 4),}
        optional = {
            'min': 0x00,
            'max': 0xff,
            'repeats': 0,
            'seed': None,
        }
        obj = un.UnitNoise(**required)
        for attr in required:
            assert getattr(obj, attr) == required[attr]
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    def test_init_all_optional(self):
        """Given optional parameters, :class:`UnitNoise` should
        initialize the given attributes with the given values.
        """
        required = {'unit': (4, 4, 4),}
        optional = {
            'min': 0x70,
            'max': 0x8f,
            'repeats': 3,
            'seed': 'spam',
        }
        obj = un.UnitNoise(**required, **optional)
        for attr in required:
            assert getattr(obj, attr) == required[attr]
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    def test_init_seeded_table(self):
        """Given a seed value, :class:`UnitNoise` should use that seed
        value to initialize its table with randomly generated values.
        """
        noise = un.UnitNoise(
            unit=(4, 4, 4), min=0, max=6, repeats=1, seed='spam'
        )
        assert noise._table == [3, 1, 0, 2, 3, 5, 0, 2, 1, 5, 4, 4]

    def test_fill(self):
        """Given the size of each dimension of the noise,
        :meth:`UnitNoise.fill` should return an array that
        contains the expected noise.
        """
        noise = un.UnitNoise((4, 4, 4), seed='spam')
        result = noise.fill((3, 8, 8))
        assert (mkhex(result) == np.array([
            [
                [0x60, 0x5d, 0x5a, 0x57, 0x54, 0x56, 0x58, 0x5a],
                [0x5f, 0x5e, 0x5e, 0x5e, 0x5e, 0x58, 0x52, 0x4c],
                [0x5e, 0x60, 0x63, 0x66, 0x69, 0x5b, 0x4d, 0x3f],
                [0x5d, 0x62, 0x68, 0x6e, 0x74, 0x5e, 0x47, 0x31],
                [0x5c, 0x64, 0x6d, 0x76, 0x7f, 0x60, 0x42, 0x24],
                [0x46, 0x4e, 0x57, 0x5f, 0x67, 0x5d, 0x53, 0x49],
                [0x31, 0x38, 0x40, 0x48, 0x50, 0x5a, 0x64, 0x6f],
                [0x1b, 0x22, 0x2a, 0x31, 0x38, 0x57, 0x75, 0x94],
            ],
            [
                [0x49, 0x48, 0x48, 0x47, 0x47, 0x55, 0x63, 0x72],
                [0x57, 0x56, 0x55, 0x54, 0x53, 0x5a, 0x62, 0x69],
                [0x64, 0x63, 0x62, 0x61, 0x60, 0x60, 0x60, 0x60],
                [0x72, 0x71, 0x6f, 0x6e, 0x6c, 0x65, 0x5e, 0x58],
                [0x80, 0x7e, 0x7c, 0x7a, 0x79, 0x6b, 0x5d, 0x4f],
                [0x70, 0x6e, 0x6c, 0x69, 0x67, 0x65, 0x64, 0x62],
                [0x61, 0x5e, 0x5b, 0x59, 0x56, 0x60, 0x6b, 0x75],
                [0x51, 0x4e, 0x4b, 0x48, 0x45, 0x5b, 0x72, 0x88],
            ],
            [
                [0x33, 0x34, 0x36, 0x38, 0x3a, 0x55, 0x6f, 0x8a],
                [0x4f, 0x4d, 0x4c, 0x4a, 0x48, 0x5d, 0x71, 0x86],
                [0x6b, 0x66, 0x61, 0x5c, 0x56, 0x65, 0x73, 0x82],
                [0x88, 0x7f, 0x76, 0x6d, 0x64, 0x6d, 0x76, 0x7e],
                [0xa4, 0x98, 0x8b, 0x7f, 0x73, 0x75, 0x78, 0x7a],
                [0x9a, 0x8e, 0x81, 0x74, 0x67, 0x6e, 0x74, 0x7b],
                [0x91, 0x83, 0x76, 0x69, 0x5c, 0x67, 0x71, 0x7b],
                [0x87, 0x79, 0x6c, 0x5f, 0x51, 0x5f, 0x6e, 0x7c],
            ],
        ], dtype=np.uint8)).all()


# Tests for CosineCurtains.
def test_CosineCurtain_fill():
    """When given the size of the image data to fill,
    :meth:`CosineCurtains.fill` should return an array
    filled with randomized data that looks somewhat
    like curtains.
    """
    noise = un.CosineCurtains((4, 4, 4), seed='spam')
    result = noise.fill((3, 8, 8))
    assert (mkhex(result) == np.array([
        [
            [0x60, 0x5e, 0x5a, 0x55, 0x54, 0x55, 0x58, 0x5a],
            [0x60, 0x5e, 0x5a, 0x55, 0x54, 0x55, 0x58, 0x5a],
            [0x60, 0x5e, 0x5a, 0x55, 0x54, 0x55, 0x58, 0x5a],
            [0x60, 0x5e, 0x5a, 0x55, 0x54, 0x55, 0x58, 0x5a],
            [0x60, 0x5e, 0x5a, 0x55, 0x54, 0x55, 0x58, 0x5a],
            [0x60, 0x5e, 0x5a, 0x55, 0x54, 0x55, 0x58, 0x5a],
            [0x60, 0x5e, 0x5a, 0x55, 0x54, 0x55, 0x58, 0x5a],
            [0x60, 0x5e, 0x5a, 0x55, 0x54, 0x55, 0x58, 0x5a],
        ],
        [
            [0x5f, 0x5e, 0x5c, 0x5b, 0x5a, 0x58, 0x54, 0x51],
            [0x5f, 0x5e, 0x5c, 0x5b, 0x5a, 0x58, 0x54, 0x51],
            [0x5f, 0x5e, 0x5c, 0x5b, 0x5a, 0x58, 0x54, 0x51],
            [0x5f, 0x5e, 0x5c, 0x5b, 0x5a, 0x58, 0x54, 0x51],
            [0x5f, 0x5e, 0x5c, 0x5b, 0x5a, 0x58, 0x54, 0x51],
            [0x5f, 0x5e, 0x5c, 0x5b, 0x5a, 0x58, 0x54, 0x51],
            [0x5f, 0x5e, 0x5c, 0x5b, 0x5a, 0x58, 0x54, 0x51],
            [0x5f, 0x5e, 0x5c, 0x5b, 0x5a, 0x58, 0x54, 0x51],
        ],
        [
            [0x5e, 0x5f, 0x63, 0x67, 0x69, 0x61, 0x4d, 0x39],
            [0x5e, 0x5f, 0x63, 0x67, 0x69, 0x61, 0x4d, 0x39],
            [0x5e, 0x5f, 0x63, 0x67, 0x69, 0x61, 0x4d, 0x39],
            [0x5e, 0x5f, 0x63, 0x67, 0x69, 0x61, 0x4d, 0x39],
            [0x5e, 0x5f, 0x63, 0x67, 0x69, 0x61, 0x4d, 0x39],
            [0x5e, 0x5f, 0x63, 0x67, 0x69, 0x61, 0x4d, 0x39],
            [0x5e, 0x5f, 0x63, 0x67, 0x69, 0x61, 0x4d, 0x39],
            [0x5e, 0x5f, 0x63, 0x67, 0x69, 0x61, 0x4d, 0x39],
        ],
    ], dtype=np.uint8)).all()


# Tests for Curtains.
def test_Curtains_fill():
    """When given the size of the image data to fill,
    :meth:`Curtains.fill` should return an array
    filled with randomized data that looks somewhat
    like curtains.
    """
    noise = un.Curtains((2, 2, 2), seed='spam')
    result = noise.fill((3, 8, 8))
    assert (mkhex(result) == np.array([
        [
            [0x60, 0x5a, 0x54, 0x58, 0x5c, 0x6d, 0x7f, 0x42],
            [0x60, 0x5a, 0x54, 0x58, 0x5c, 0x6d, 0x7f, 0x42],
            [0x60, 0x5a, 0x54, 0x58, 0x5c, 0x6d, 0x7f, 0x42],
            [0x60, 0x5a, 0x54, 0x58, 0x5c, 0x6d, 0x7f, 0x42],
            [0x60, 0x5a, 0x54, 0x58, 0x5c, 0x6d, 0x7f, 0x42],
            [0x60, 0x5a, 0x54, 0x58, 0x5c, 0x6d, 0x7f, 0x42],
            [0x60, 0x5a, 0x54, 0x58, 0x5c, 0x6d, 0x7f, 0x42],
            [0x60, 0x5a, 0x54, 0x58, 0x5c, 0x6d, 0x7f, 0x42],
        ],
        [
            [0x33, 0x36, 0x3a, 0x6f, 0xa4, 0x8b, 0x73, 0x78],
            [0x33, 0x36, 0x3a, 0x6f, 0xa4, 0x8b, 0x73, 0x78],
            [0x33, 0x36, 0x3a, 0x6f, 0xa4, 0x8b, 0x73, 0x78],
            [0x33, 0x36, 0x3a, 0x6f, 0xa4, 0x8b, 0x73, 0x78],
            [0x33, 0x36, 0x3a, 0x6f, 0xa4, 0x8b, 0x73, 0x78],
            [0x33, 0x36, 0x3a, 0x6f, 0xa4, 0x8b, 0x73, 0x78],
            [0x33, 0x36, 0x3a, 0x6f, 0xa4, 0x8b, 0x73, 0x78],
            [0x33, 0x36, 0x3a, 0x6f, 0xa4, 0x8b, 0x73, 0x78],
        ],
        [
            [0x06, 0x13, 0x21, 0x87, 0xed, 0xaa, 0x67, 0xae],
            [0x06, 0x13, 0x21, 0x87, 0xed, 0xaa, 0x67, 0xae],
            [0x06, 0x13, 0x21, 0x87, 0xed, 0xaa, 0x67, 0xae],
            [0x06, 0x13, 0x21, 0x87, 0xed, 0xaa, 0x67, 0xae],
            [0x06, 0x13, 0x21, 0x87, 0xed, 0xaa, 0x67, 0xae],
            [0x06, 0x13, 0x21, 0x87, 0xed, 0xaa, 0x67, 0xae],
            [0x06, 0x13, 0x21, 0x87, 0xed, 0xaa, 0x67, 0xae],
            [0x06, 0x13, 0x21, 0x87, 0xed, 0xaa, 0x67, 0xae],
        ],
    ], dtype=np.uint8)).all()


# Tests for OctaveCosineCurtains.
class TestOctaveCosineCurtains:
    def test_init_all_default(self):
        """Given no parameters, :class:`OctaveCosineCurtains`
        should initialize the optional attributes with default
        values.
        """
        optional = {
            'octaves': 4,
            'persistence': 8,
            'amplitude': 8,
            'frequency': 2,
            'unit': (1024, 1024, 1024),
            'min': 0x00,
            'max': 0xff,
            'repeats': 1,
            'seed': None,
        }
        obj = un.OctaveCosineCurtains()
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    def test_init_all_optional(self):
        """Given optional parameters, :class:`OctaveCosineCurtains`
        should initialize the given attributes with the given values.
        """
        optional = {
            'octaves':3,
            'persistence': 4,
            'amplitude': 5,
            'frequency': 6,
            'unit': (4, 4, 4),
            'min': 0x70,
            'max': 0x8f,
            'repeats': 3,
            'seed': 'spam',
        }
        obj = un.OctaveCosineCurtains(**optional)
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    def test_fill(self):
        """When given the size of the image data to fill,
        :meth:`OctaveCosineCurtains.fill` should return an
        array filled with randomized data that looks somewhat
        like curtains.
        """
        noise = un.OctaveCosineCurtains(unit=(4, 4, 4), seed='spam')
        result = noise.fill((3, 8, 8))
        assert (mkhex(result) == np.array([
            [
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
            ],
            [
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
            ],
            [
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
            ],
        ], dtype=np.uint8)).all()


class TestOctaveCurtains:
    def test_init_all_default(self):
        """Given no parameters, :class:`OctaveCurtains`
        should initialize the optional attributes with
        default values.
        """
        optional = {
            'octaves': 4,
            'persistence': 8,
            'amplitude': 8,
            'frequency': 2,
            'unit': (1024, 1024, 1024),
            'min': 0x00,
            'max': 0xff,
            'repeats': 1,
            'seed': None,
        }
        obj = un.OctaveCurtains()
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    def test_init_all_optional(self):
        """Given optional parameters, :class:`OctaveCurtains`
        should initialize the given attributes with the given
        values.
        """
        optional = {
            'octaves':3,
            'persistence': 4,
            'amplitude': 5,
            'frequency': 6,
            'unit': (4, 4, 4),
            'min': 0x70,
            'max': 0x8f,
            'repeats': 3,
            'seed': 'spam',
        }
        obj = un.OctaveCurtains(**optional)
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    def test_fill(self):
        """When given the size of the image data to fill,
        :meth:`OctaveCosineCurtains.fill` should return an
        array filled with randomized data that looks somewhat
        like curtains.
        """
        noise = un.OctaveCurtains(unit=(4, 4, 4), seed='spam')
        result = noise.fill((3, 8, 8))
        assert (mkhex(result) == np.array([
            [
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
            ],
            [
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
            ],
            [
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
            ],
        ], dtype=np.uint8)).all()


class TestOctaveUnitNoise:
    def test_init_all_default(self):
        """Given no parameters, :class:`OctaveUnitNoise`
        should initialize the optional attributes with
        default values.
        """
        optional = {
            'octaves': 4,
            'persistence': 8,
            'amplitude': 8,
            'frequency': 2,
            'unit': (1024, 1024, 1024),
            'min': 0x00,
            'max': 0xff,
            'repeats': 1,
            'seed': None,
        }
        obj = un.OctaveUnitNoise()
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    def test_init_all_optional(self):
        """Given optional parameters, :class:`OctaveUnitNoise`
        should initialize the given attributes with the given
        values.
        """
        optional = {
            'octaves':3,
            'persistence': 4,
            'amplitude': 5,
            'frequency': 6,
            'unit': (4, 4, 4),
            'min': 0x70,
            'max': 0x8f,
            'repeats': 3,
            'seed': 'spam',
        }
        obj = un.OctaveUnitNoise(**optional)
        for attr in optional:
            assert getattr(obj, attr) == optional[attr]

    def test_fill(self):
        """When given the size of the image data to fill,
        :meth:`OctaveUnitNoise.fill` should return an
        array filled with randomized data that looks somewhat
        like curtains.
        """
        noise = un.OctaveUnitNoise(unit=(4, 4, 4), seed='spam')
        result = noise.fill((3, 8, 8))
        assert (mkhex(result) == np.array([
            [
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x80, 0x65, 0xba, 0x92, 0x63, 0x92, 0x80, 0x49],
                [0x51, 0xcf, 0x54, 0x74, 0x54, 0x54, 0x72, 0x5b],
                [0x89, 0xb3, 0x70, 0x8b, 0x55, 0x3f, 0x90, 0x8f],
                [0xb5, 0x75, 0xc4, 0x94, 0x84, 0x88, 0x7b, 0x7a],
                [0x72, 0x92, 0x61, 0xa8, 0x55, 0x46, 0x64, 0x63],
            ],
            [
                [0x76, 0x42, 0xa2, 0x51, 0x27, 0x46, 0x66, 0x73],
                [0x6e, 0x64, 0x81, 0x4c, 0x80, 0x79, 0x66, 0xcd],
                [0x77, 0x55, 0xab, 0x98, 0x7a, 0xa9, 0x99, 0x6f],
                [0x5d, 0x8e, 0x67, 0x64, 0xd5, 0xd0, 0x5a, 0x52],
                [0x9b, 0x63, 0xa2, 0x3c, 0x3b, 0x3f, 0x9a, 0x7b],
                [0x81, 0x4a, 0xb6, 0x7b, 0x60, 0xdd, 0x3b, 0x55],
                [0x96, 0xa8, 0x89, 0x68, 0x85, 0x82, 0x76, 0x6f],
                [0x75, 0x59, 0x99, 0x8a, 0x55, 0x76, 0x46, 0x9e],
            ],
            [
                [0x68, 0xa2, 0x80, 0x54, 0x89, 0x79, 0xd3, 0x8c],
                [0x5d, 0x59, 0x44, 0xb4, 0x45, 0x98, 0xbb, 0xbc],
                [0x33, 0xc1, 0x7f, 0x9b, 0x18, 0x74, 0x87, 0x5b],
                [0xa0, 0x9c, 0x83, 0x67, 0x79, 0x3e, 0x92, 0x82],
                [0x4f, 0x86, 0x67, 0x63, 0x87, 0x7f, 0xc2, 0xad],
                [0x4b, 0xd7, 0x27, 0x38, 0x97, 0x4b, 0x8f, 0x51],
                [0x70, 0x9b, 0x4a, 0x8a, 0xa1, 0xa9, 0x46, 0x89],
                [0x80, 0xc3, 0x6c, 0x87, 0x41, 0x14, 0x91, 0x34],
            ],
        ], dtype=np.uint8)).all()


# Tests for octave_noise_factory.
class TestOctaveNoiseFactory:
    def test_result_has_source(self):
        """Subclasses of :class:`OctaveNoise` must identify a
        :class:`UnitNoise` subclass for the creation of octave
        noise.
        """
        cls = un.octave_noise_factory(un.UnitNoise, un.OctaveNoiseDefaults())
        assert cls.source == un.UnitNoise

    def test_set_attr_defaults(self):
        """Created subclasses of :class:`OctaveNoise` should set the octave
        noise parameter and unit noise parameter defaults.
        """
        cls = un.octave_noise_factory(un.UnitNoise, un.OctaveNoiseDefaults())
        obj = cls()
        assert obj.octaves == 4
        assert obj.persistence == 8
        assert obj.amplitude == 8
        assert obj.frequency == 2
        assert obj.unit == (1024, 1024, 1024)
        assert obj.min == 0x00
        assert obj.max == 0xff
        assert obj.repeats == 1
        assert obj.seed is None

    def test_set_fill(self):
        """Created subclasses of :class:`OctaveNoise` should have a
        fill method that generates octave unit noise.
        """
        cls = un.octave_noise_factory(un.UnitNoise, un.OctaveNoiseDefaults())
        noise = cls(unit=(4, 4, 4), seed='spam')
        result = noise.fill((3, 8, 8))
        assert (mkhex(result) == np.array([
            [
                [0xae, 0x5d, 0x63, 0x87, 0x78, 0x40, 0x73, 0x45],
                [0x83, 0x77, 0x42, 0x57, 0x65, 0x80, 0x54, 0x52],
                [0x66, 0x79, 0x5c, 0xb9, 0x7e, 0xb5, 0x77, 0xbb],
                [0x80, 0x65, 0xba, 0x92, 0x63, 0x92, 0x80, 0x49],
                [0x51, 0xcf, 0x54, 0x74, 0x54, 0x54, 0x72, 0x5b],
                [0x89, 0xb3, 0x70, 0x8b, 0x55, 0x3f, 0x90, 0x8f],
                [0xb5, 0x75, 0xc4, 0x94, 0x84, 0x88, 0x7b, 0x7a],
                [0x72, 0x92, 0x61, 0xa8, 0x55, 0x46, 0x64, 0x63],
            ],
            [
                [0x76, 0x42, 0xa2, 0x51, 0x27, 0x46, 0x66, 0x73],
                [0x6e, 0x64, 0x81, 0x4c, 0x80, 0x79, 0x66, 0xcd],
                [0x77, 0x55, 0xab, 0x98, 0x7a, 0xa9, 0x99, 0x6f],
                [0x5d, 0x8e, 0x67, 0x64, 0xd5, 0xd0, 0x5a, 0x52],
                [0x9b, 0x63, 0xa2, 0x3c, 0x3b, 0x3f, 0x9a, 0x7b],
                [0x81, 0x4a, 0xb6, 0x7b, 0x60, 0xdd, 0x3b, 0x55],
                [0x96, 0xa8, 0x89, 0x68, 0x85, 0x82, 0x76, 0x6f],
                [0x75, 0x59, 0x99, 0x8a, 0x55, 0x76, 0x46, 0x9e],
            ],
            [
                [0x68, 0xa2, 0x80, 0x54, 0x89, 0x79, 0xd3, 0x8c],
                [0x5d, 0x59, 0x44, 0xb4, 0x45, 0x98, 0xbb, 0xbc],
                [0x33, 0xc1, 0x7f, 0x9b, 0x18, 0x74, 0x87, 0x5b],
                [0xa0, 0x9c, 0x83, 0x67, 0x79, 0x3e, 0x92, 0x82],
                [0x4f, 0x86, 0x67, 0x63, 0x87, 0x7f, 0xc2, 0xad],
                [0x4b, 0xd7, 0x27, 0x38, 0x97, 0x4b, 0x8f, 0x51],
                [0x70, 0x9b, 0x4a, 0x8a, 0xa1, 0xa9, 0x46, 0x89],
                [0x80, 0xc3, 0x6c, 0x87, 0x41, 0x14, 0x91, 0x34],
            ],
        ], dtype=np.uint8)).all
