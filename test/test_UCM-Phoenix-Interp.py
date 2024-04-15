# -*- coding: utf-8 -*-
"""
@author: negar_hofism7
"""
import unittest
import numpy as np
from UCM_Phoenix_Interp import interp  # Adjust the import according to your actual module name and structure

class TestInterpFunction(unittest.TestCase):
    def test_basic_interpolation(self):
        # Test basic linear interpolation
        x = np.array([0, 10])
        t = np.array([0, 10])
        T = np.array([5])
        expected = np.array([5])
        result = interp(x, t, T)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

    def test_out_of_bounds(self):
        # Test values outside the bounds of t
        x = np.array([0, 10, 20])
        t = np.array([0, 10, 20])
        T = np.array([-5, 30])
        expected = np.array([0, 20])  # Assuming extrapolation not handled, so clamp to nearest values
        result = interp(x, t, T)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

    def test_non_uniform_spacing(self):
        # Test non-uniform spacing in t
        x = np.array([0, 10, 25])
        t = np.array([0, 5, 20])
        T = np.array([10])
        expected = np.array([15])
        result = interp(x, t, T)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

if __name__ == '__main__':
    unittest.main()

