class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        table = {}
        l = len(s)
        if len(set(s)) != len(set(t)):
            return False
        
        for i in range(l):
            if s[i] in table:
                if table[s[i]] != t[i]:
                    return False
            else:
                table[s[i]] = t[i]
        return True