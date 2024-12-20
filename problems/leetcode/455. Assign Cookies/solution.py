#
class Solution:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        res = 0
        i, j = len(g)-1, len(s)-1
        g.sort()
        s.sort()

        while j >= 0 and i >= 0:
            if s[j] >= g[i]:
                i -= 1
                j -= 1
                res += 1
            else:
                i -= 1
        
        return res