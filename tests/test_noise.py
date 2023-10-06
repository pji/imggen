"""
test_noise
~~~~~~~~~~

Unit tests for the imggen.noise module.
"""
import numpy as np

from imggen import noise as n


# Test fpr initialization.
def test_init_required():
    """When given no parameters, :class:`Noise` should initialize a new
    object with default attribute values.
    """
    optionals = {'seed': None,}
    obj = n.Noise()
    for attr in optionals:
        assert getattr(obj, attr) == optionals[attr]


def test_init_optional():
    """When given parameters, :class:`Noise` should initialize a new
    object setting attributes to the given values.
    """
    optionals = {'seed': 'spam',}
    obj = n.Noise(**optionals)
    for attr in optionals:
        assert getattr(obj, attr) == optionals[attr]


# Tests for fill.
def test_fill():
    """When given the size of an array, :meth:`Noise.fill` should return
    an array that contains randomly generated noise.
    """
    noise = n.Noise(seed='spam')
    result = noise.fill((2, 8, 8))
    assert ((result * 0xff).astype(np.uint8) == np.array([
        [
            [0xb6, 0xe0, 0xc4, 0x94, 0x3e, 0x0a, 0xc6, 0x8c],
            [0xb2, 0x14, 0x1f, 0x1f, 0x3e, 0x2e, 0x08, 0x92],
            [0xaa, 0xb6, 0x9d, 0x57, 0xf4, 0xb7, 0xba, 0x1c],
            [0x52, 0x89, 0xe5, 0xdb, 0x7d, 0xc7, 0x52, 0x2b],
            [0x15, 0xc4, 0xb9, 0x46, 0xca, 0x44, 0x01, 0xae],
            [0x48, 0xee, 0x63, 0x8b, 0xf7, 0xbc, 0xa5, 0x0a],
            [0x8c, 0x21, 0xf7, 0x71, 0x99, 0x2c, 0xa9, 0x8a],
            [0x99, 0xa8, 0xba, 0xd9, 0x0b, 0xd8, 0x85, 0xc9],
        ],
        [
            [0xe4, 0x10, 0xc0, 0xf3, 0xf5, 0x17, 0xf4, 0x93],
            [0xd7, 0x72, 0x80, 0xd2, 0x6a, 0xc8, 0x5d, 0xee],
            [0xb7, 0xce, 0x10, 0x27, 0x7d, 0x7f, 0xe5, 0xfd],
            [0x5d, 0x91, 0xb4, 0x01, 0x78, 0x02, 0x5d, 0x1b],
            [0x04, 0x20, 0xb8, 0x23, 0x50, 0xc2, 0x67, 0x45],
            [0x94, 0x12, 0x72, 0x00, 0x67, 0x22, 0x63, 0xa4],
            [0x66, 0x79, 0x77, 0xa5, 0xf8, 0xcf, 0x46, 0xc2],
            [0xe6, 0x73, 0xa0, 0xa5, 0xb4, 0x16, 0x04, 0x4c],
        ],
    ], dtype=np.uint8)).all()


def test_fill_different_seed_different_noise():
    """When given different seeds, two instances of :class:`Noise`
    should return different noise.
    """
    a = n.Noise('spam')
    b = n.Noise('eggs')
    shape = (2, 8, 8)
    assert not (a.fill(shape) == b.fill(shape)).all()


def test_fill_same_seed_same_noise():
    """When given the same seeds, two instances of :class:`Noise`
    should return the same noise.
    """
    a = n.Noise('spam')
    b = n.Noise('spam')
    shape = (2, 8, 8)
    assert (a.fill(shape) == b.fill(shape)).all()


def test_fill_no_seed_different_noise():
    """When given no seeds, two instances of :class:`Noise`
    should return different noise.

    .. note:
        This test is not deterministic. It's theoretically possible
        for this test to fail because the output of the unseeded
        random number generator is not predictable. This should be
        extremely unlikely.
    """
    a = n.Noise()
    b = n.Noise()
    shape = (2, 8, 8)
    assert not (a.fill(shape) == b.fill(shape)).all()
