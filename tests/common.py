"""
common
~~~~~~

Common code used in multiple test modules
"""
import unittest as ut

import numpy as np


# Utility functions.
def mkhex(a):
    return (a * 0xff).astype(np.uint8)


# Base test cases.
class ArrayTestCase(ut.TestCase):
    def assertArrayEqual(self, a, b):
        """Assert that two numpy.ndarrays are equal."""
        a_list = a.tolist()
        b_list = b.tolist()
        self.assertListEqual(a_list, b_list)

    def assertArrayNotEqual(self, a, b):
        """Assert that two numpy.ndarrays are not equal."""
        a_list = a.tolist()
        b_list = b.tolist()
        self.assertFalse(a_list == b_list)


class SourceTestCase(ArrayTestCase):
    def fill_test(self, exp, source, kwargs, size=None):
        # Run test.
        obj = source(**kwargs)
        if not size:
            size = exp.shape
        result = obj.fill(size)

        # Round actual result to avoid having to type out long float
        # numbers in the expected result.
        act = (result * 0xff).astype(np.uint8)

        # Determine test result.
        self.assertArrayEqual(exp, act)
