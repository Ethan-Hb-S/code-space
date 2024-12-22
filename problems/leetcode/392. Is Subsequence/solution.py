# Hashmap Solution
# Time Complexity: O(n)
# Space Complexity: O(n)
# class Solution:
#     def isSubsequence(self, s: str, t: str) -> bool:
#         table = {}
#         index = 0

#         for i in s:
#             indice = table.setdefault(i, set([index]))
#             if indice:
#                 indice.add(index)
#             index += 1

#         p_index = 0
#         for i in t:
#             if i in table and p_index in table[i]:
#                 table[i].discard(p_index)
#                 p_index += 1

#         return p_index == index


# Dynamic Programming Solution
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if len(s) > len(t):
            return False
        if not len(s):
            return True
        
        dp = [0] * (1 + len(t))
        
        for i in range(1, len(t) + 1):
            if t[i-1] == s[dp[i-1]]:
                dp[i] = dp[i-1] + 1
            else:
                dp[i] = dp[i-1]
            
            if dp[i] >= len(s):
                return True

        return False