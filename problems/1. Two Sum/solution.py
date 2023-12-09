class Solution:
    # Time: O(n^2)
    # Space: O(1)
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        for i in nums:
            x = nums.index(i)
            for j in nums[x+1:]:
                if i + j == target:
                    if i == j:
                        return [x, nums.index(j, x+1)]
                    return [x, nums.index(j)]
                
class Solution_Improved:
    # With hashmap (dictionary in Python)
    # Time: O(n)
    # Space: O(n)
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        # list.index() takes O(n), so better just simply to use indices here
        hashmap = {}
        for i in range(len(nums)):
            value = nums[i]
            diff = target - value
            # 'diff in hashmap.keys()' can be (very) slightly faster than 'diff in hashmap' (usually no differeces)
            if diff in hashmap:
                return [hashmap[diff], i]
            hashmap[value] = i