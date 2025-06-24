from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Given an array of integers nums and an integer target, return indices 
        of the two numbers such that they add up to target.
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        seen = {}  # value -> index mapping
        
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        
        return []  # No solution found (shouldn't happen per problem constraints)