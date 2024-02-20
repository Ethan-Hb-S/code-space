class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        
        copy = nums[:]
        l = len(nums)
        for i in range(l):
            nums[ (i + k) % l ] = copy[i]