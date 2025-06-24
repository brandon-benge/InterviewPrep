#!/usr/bin/env python3
"""
Unit tests for the Two Sum problem using Python's unittest framework.
Run with: python -m unittest test_two_sum_unittest.py
"""

import unittest
import sys
import os

# Add the current directory to Python path so we can import two_sum
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from two_sum import Solution

class TestTwoSum(unittest.TestCase):
    """Unit tests for Two Sum solution."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.solution = Solution()
    
    def test_basic_cases(self):
        """Test basic functionality."""
        # LeetCode example
        result = self.solution.twoSum([2, 7, 11, 15], 9)
        self.assertEqual(sorted(result), [0, 1])
        
        # Different order
        result = self.solution.twoSum([3, 2, 4], 6)
        self.assertEqual(sorted(result), [1, 2])
    
    def test_duplicate_numbers(self):
        """Test with duplicate numbers."""
        result = self.solution.twoSum([3, 3], 6)
        self.assertEqual(sorted(result), [0, 1])
    
    def test_zero_target(self):
        """Test when target is zero."""
        result = self.solution.twoSum([0, 4, 3, 0], 0)
        self.assertEqual(sorted(result), [0, 3])
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        result = self.solution.twoSum([-1, -2, -3, -4, -5], -8)
        self.assertEqual(sorted(result), [2, 4])
    
    def test_large_numbers(self):
        """Test with large numbers."""
        result = self.solution.twoSum([5, 75, 25], 100)
        self.assertEqual(sorted(result), [1, 2])
    
    def test_result_validity(self):
        """Test that results are always valid."""
        test_cases = [
            ([2, 7, 11, 15], 9),
            ([3, 2, 4], 6),
            ([1, 3, 7, 9, 2], 11),
            ([-3, 4, 3, 90], 0),
        ]
        
        for nums, target in test_cases:
            with self.subTest(nums=nums, target=target):
                result = self.solution.twoSum(nums, target)
                
                # Check that we got exactly 2 indices
                self.assertEqual(len(result), 2)
                
                # Check that indices are different
                self.assertNotEqual(result[0], result[1])
                
                # Check that indices are valid
                self.assertGreaterEqual(result[0], 0)
                self.assertGreaterEqual(result[1], 0)
                self.assertLess(result[0], len(nums))
                self.assertLess(result[1], len(nums))
                
                # Check that the sum is correct
                actual_sum = nums[result[0]] + nums[result[1]]
                self.assertEqual(actual_sum, target)

if __name__ == '__main__':
    unittest.main()
