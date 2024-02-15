class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        k = len(nums)
        i = 0
        while i < k:
            if nums[i] == val:
                nums[i] = nums[k-1]
                nums[k-1] = val
                k -= 1
            else:
                i += 1
        
        return k