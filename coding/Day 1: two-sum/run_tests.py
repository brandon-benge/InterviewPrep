#!/usr/bin/env python3
"""
Simple test runner for Two Sum using external test data.
This approach separates the solution, test data, and test execution.
"""

from two_sum import Solution
from test_data import TEST_CASES, SIMPLE_CASES

def run_tests(test_cases, test_name="Tests"):
    """Run a set of test cases and report results."""
    solution = Solution()
    print(f"\n🧪 Running {test_name}...")
    print("=" * 50)
    
    passed = 0
    total = len(test_cases)
    
    for i, (nums, target, expected, description) in enumerate(test_cases, 1):
        result = solution.twoSum(nums, target)
        
        # Validate result
        is_correct = (
            len(result) == 2 and
            result[0] != result[1] and
            0 <= result[0] < len(nums) and
            0 <= result[1] < len(nums) and
            nums[result[0]] + nums[result[1]] == target
        )
        
        if is_correct:
            passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        print(f"Test {i:2d}: {status} - {description}")
        if not is_correct:
            print(f"    Input: {nums}, target={target}")
            print(f"    Got: {result}")
    
    print(f"\nResults: {passed}/{total} passed")
    return passed == total

def main():
    """Run all test suites."""
    print("Two Sum Solution Tester")
    print("=" * 50)
    
    # Run simple tests first
    simple_passed = run_tests(SIMPLE_CASES, "Quick Tests")
    
    # Run full test suite
    full_passed = run_tests(TEST_CASES, "Full Test Suite")
    
    print("\n" + "=" * 50)
    if simple_passed and full_passed:
        print("🎉 All tests passed! Your solution is working correctly.")
    else:
        print("❌ Some tests failed. Check your implementation.")

if __name__ == "__main__":
    main()
