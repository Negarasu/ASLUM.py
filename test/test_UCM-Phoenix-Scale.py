# -*- coding: utf-8 -*-
"""
@author: negar_hofism7
"""
import unittest
import numpy as np
from UCM_Phoenix_Scale import scale  # Adjust the import according to your actual module name and structure

class TestScaleFunction(unittest.TestCase):
    def test_basic_resampling(self):
        # Scenario where t_scale perfectly aligns with t
        x = np.array([1, 2, 3, 4, 5])
        t = np.array([0, 1, 2, 3, 4])
        t_scale = np.array([0, 2, 4])
        expected = np.array([1, 3, 5])
        result = scale(x, t, t_scale)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

    def test_resampling_with_averaging(self):
        # t_scale results in averaging intervals in x
        x = np.array([1, 2, 3, 4, 5, 6])
        t = np.array([0, 1, 2, 3, 4, 5])
        t_scale = np.array([0, 3, 5])
        expected = np.array([1.5, 4, 5.5])  # Averages of [1, 2], [3, 4, 5], [6]
        result = scale(x, t, t_scale)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

    def test_out_of_bounds_resampling(self):
        # t_scale includes times beyond the range of t
        x = np.array([1, 2, 3])
        t = np.array([0, 1, 2])
        t_scale = np.array([-1, 0, 1, 2, 3])
        expected = np.array([np.nan, 1, 2, 3, np.nan])  # Assuming out of bounds returns nan
        result = scale(x, t, t_scale)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

if __name__ == '__main__':
    unittest.main()

