# -*- coding: utf-8 -*-
"""
@author: negar_hofism7
"""
import unittest
import numpy as np
from functions import Keff, Zenith, Viewfac, Green  # Adjust the import according to your actual module name and structure

class TestEngineeringFunctions(unittest.TestCase):
    def test_Keff(self):
        # Simple case with uniform properties
        d = np.array([0.5, 0.5])
        k = np.array([1, 2])
        n = 2
        expected = np.array([0.66666667, 2])
        result = Keff(d, k, n)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

    def test_Zenith(self):
        # Basic test assuming known values
        day = 172  # day near summer solstice
        tS = 12    # solar noon
        phi = np.pi / 4  # 45 degrees in radians
        lam = 0
        nt = 1
        qz, qs = Zenith(day, tS, phi, lam, nt)
        self.assertTrue(np.all(qz >= 0) and np.all(qs >= 0))

    def test_Viewfac(self):
        # Geometrically simple case
        h = 1
        w = 1
        FGS, FWW, FGW, FWG, FWS = Viewfac(h, w)
        self.assertEqual(FGS, FWW)  # Symmetry in square configuration

    def test_Green(self):
        # Test with basic input
        Fo = np.array([0.1, 0.2, 0.3])
        d = 1
        k = 1
        a = 1
        t = np.array([10, 20, 30])
        n = 3
        icr = 1
        g = Green(Fo, d, k, a, t, n, icr)
        self.assertEqual(g.shape, (3, 2))  # Should return a matrix with 3 rows and 2 columns

if __name__ == '__main__':
    unittest.main()

