#!/usr/bin/env python3
"""
Test cases for the Two Sum problem.
Run this file to test the two_sum.py solution.
"""

from two_sum import Solution

def test_two_sum():
    """Test the twoSum function with various test cases."""
    solution = Solution()
    
    # Test cases: (nums, target, expected_result, description)
    test_cases = [
        # Basic cases
        ([2, 7, 11, 15], 9, [0, 1], "Basic case from LeetCode example"),
        ([3, 2, 4], 6, [1, 2], "Target not at indices 0,1"),
        ([3, 3], 6, [0, 1], "Duplicate numbers"),
        
        # Edge cases
        ([0, 4, 3, 0], 0, [0, 3], "Target is zero"),
        ([-1, -2, -3, -4, -5], -8, [2, 4], "All negative numbers"),
        ([1, 2, 3, 4, 5], 8, [2, 4], "Sequential array"),
        
        # Larger arrays
        ([1, 3, 7, 9, 2], 11, [2, 3], "Unsorted array"),
        ([5, 75, 25], 100, [1, 2], "Large numbers"),
        
        # Additional edge cases
        ([1, 1, 1, 1, 1, 4, 1, 1, 1], 5, [0, 5], "Many duplicates"),
        ([-3, 4, 3, 90], 0, [0, 2], "Negative and positive sum to zero"),
    ]
    
    print("Running Two Sum Tests...")
    print("=" * 50)
    
    passed = 0
    total = len(test_cases)
    
    for i, (nums, target, expected, description) in enumerate(test_cases, 1):
        result = solution.twoSum(nums, target)
        
        # Check if result is correct (order might be different)
        is_correct = (
            len(result) == 2 and
            result[0] != result[1] and  # Different indices
            0 <= result[0] < len(nums) and  # Valid indices
            0 <= result[1] < len(nums) and
            nums[result[0]] + nums[result[1]] == target  # Correct sum
        )
        
        if is_correct:
            passed += 1
            status = "✓ PASS"
        else:
            status = "✗ FAIL"
        
        print(f"Test {i:2d}: {status}")
        print(f"  Description: {description}")
        print(f"  Input: nums={nums}, target={target}")
        print(f"  Expected: indices that sum to {target}")
        print(f"  Got: {result}")
        
        if is_correct and len(result) == 2:
            print(f"  Verification: nums[{result[0]}] + nums[{result[1]}] = {nums[result[0]]} + {nums[result[1]]} = {nums[result[0]] + nums[result[1]]}")
        elif not is_correct:
            print(f"  ERROR: Invalid result!")
        
        print()
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"❌ {total - passed} tests failed.")
    
    return passed == total

if __name__ == "__main__":
    test_two_sum()
