class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = len(nums)
        i = 1
        while i < k:
            if nums[i] == nums[i-1]:
                order(nums, i, k-1)
                k -= 1
            else:
                i += 1
        return k
        
def order(nums: list, init, final):
    temp = nums[init]
    for i in range(init+1, final+1):
        nums[i-1] = nums[i]
    nums[final] = temp