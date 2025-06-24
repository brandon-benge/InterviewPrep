"""
Test data for Two Sum problem.
Import this module to get test cases for your solution.
"""

# Test cases format: (input_array, target, expected_indices, description)
TEST_CASES = [
    # Basic cases
    ([2, 7, 11, 15], 9, [0, 1], "LeetCode example 1"),
    ([3, 2, 4], 6, [1, 2], "LeetCode example 2"),
    ([3, 3], 6, [0, 1], "LeetCode example 3"),
    
    # Edge cases
    ([0, 4, 3, 0], 0, [0, 3], "Target is zero"),
    ([-1, -2, -3, -4, -5], -8, [2, 4], "All negative numbers"),
    ([1, 2, 3, 4, 5], 8, [2, 4], "Sequential positive numbers"),
    
    # Larger arrays
    ([1, 3, 7, 9, 2], 11, [2, 3], "Unsorted array"),
    ([5, 75, 25], 100, [1, 2], "Large numbers"),
    ([1, 1, 1, 1, 1, 4, 1, 1, 1], 5, [0, 5], "Many duplicates"),
    
    # Mixed positive/negative
    ([-3, 4, 3, 90], 0, [0, 2], "Negative and positive sum to zero"),
    ([10, -1, -2, 7], 8, [0, 2], "Mixed numbers"),
]

# Simple test cases for quick validation
SIMPLE_CASES = [
    ([2, 7, 11, 15], 9, [0, 1], "Basic LeetCode example"),
    ([3, 2, 4], 6, [1, 2], "Different position target"),
    ([3, 3], 6, [0, 1], "Duplicate numbers"),
]

# Edge cases for thorough testing
EDGE_CASES = [
    ([0, 4, 3, 0], 0, [0, 3], "Target is zero"),
    ([-1, -2, -3, -4, -5], -8, [2, 4], "All negative numbers"),
    ([1, 1, 1, 1, 1, 4, 1, 1, 1], 5, [0, 5], "Many duplicates"),
]
