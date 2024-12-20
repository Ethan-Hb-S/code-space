#
class Solution:
    def numTrees(self, n: int) -> int:
        if n == 0: return 1
        dp = [0] * (n + 1)
        dp[0], dp[1] = 1, 1

        for i in range(2, n+1):
            left, right = i-1, 0
            while left >= 0:
                dp[i] += (dp[left] * dp[right])
                left -= 1
                right += 1
        
        return dp[n]