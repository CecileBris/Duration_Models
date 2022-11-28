# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 19:36:12 2022

@author: ceecy
"""

import unittest
import nivetude from Couple_duration_datapreprocess

def test_nivetude():
    assert nivetude(00) == 0, "Should be 0"
    assert nivetude(20) == 1, "Should be 1"
    assert nivetude(30) == 2, "Should be 2"
    assert nivetude(40) == 3, "Should be 3"


if __name__ == "__main__":
    unittest.main()
