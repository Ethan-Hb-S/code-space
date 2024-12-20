#
class Solution:
    def countSubstrings(self, s: str) -> int:
        dp = [[True if (abs(j-i) <= 1 and s[i] == s[j]) else False for i in range(len(s))] for j in range(len(s))]
        count = 0

        for i in range(len(s)-1, -1, -1):
            for j in range(i, len(s)):
                if s[i] == s[j]:
                    if j - i <= 1:
                        count += 1
                    elif dp[i+1][j-1]:
                        dp[i][j] = True
                        count += 1

        return count
