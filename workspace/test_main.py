#!/usr/bin/env python3
# Unit tests for unique binary search trees application

import unittest
from main import uniqueBSTs

class TestUniqueBSTs(unittest.TestCase):
    # Test cases for the uniqueBSTs function
    
    def test_base_cases(self):
        # Test base cases: n = 0 and n = 1
        self.assertEqual(uniqueBSTs(0), 1)
        self.assertEqual(uniqueBSTs(1), 1)
    
    def test_small_values(self):
        # Test small values of n: n = 2, n = 3, n = 4
        self.assertEqual(uniqueBSTs(2), 2)
        self.assertEqual(uniqueBSTs(3), 5)
        self.assertEqual(uniqueBSTs(4), 14)
    
    def test_large_values(self):
        # Test large values of n: n = 10, n = 15, n = 20
        self.assertEqual(uniqueBSTs(10), 16796)
        self.assertEqual(uniqueBSTs(15), 9694845)
        self.assertEqual(uniqueBSTs(20), 6564120420)
    
    def test_invalid_input(self):
        # Test invalid input: n = -1, n = -10
        with self.assertRaises(ValueError):
            uniqueBSTs(-1)
        with self.assertRaises(ValueError):
            uniqueBSTs(-10)
    
    def test_non_integer_input(self):
        # Test non-integer input: n = 3.5, n = 10.2
        with self.assertRaises(TypeError):
            uniqueBSTs(3.5)
        with self.assertRaises(TypeError):
            uniqueBSTs(10.2)
    
    def test_performance(self):
        # Test performance: calculate uniqueBSTs(100) and verify that it takes less than 1 second
        import time
        start_time = time.time()
        uniqueBSTs(100)
        end_time = time.time()
        self.assertLess(end_time - start_time, 1)

if __name__ == "__main__":
    unittest.main()