#
class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        if len(s) == 1: return 1
        l = len(s) + 1
        dp = [[1 if i == j else 0 for j in range(l)] for i in range(l)]

        for i in range(l - 1, -1, -1):
            for j in range(i + 1, l):
                if s[i - 1] == s[j - 1]:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    dp[i][j] = max(dp[i][j - 1], dp[i + 1][j])

        return dp[1][-1]