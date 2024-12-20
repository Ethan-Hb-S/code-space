#
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = [1] * (len(nums))

        for i in range(len(nums)-1):
            for j in range(i+1, len(nums)):
                if nums[i] < nums[j] and dp[i] >= dp[j]:
                    dp[j] = dp[i] + 1
        
        return max(dp)