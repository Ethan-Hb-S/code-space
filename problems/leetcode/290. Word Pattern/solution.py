class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        table = {}
        words = s.split(' ')
        l = len(words)
        if len(words) != len(pattern) or len(set(words)) != len(set(pattern)):
            return False
        
        for i in range(l):
            if pattern[i] in table:
                if table[pattern[i]] != words[i]:
                    return False
            else:
                table[pattern[i]] = words[i]
        return True