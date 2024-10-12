class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        hashmap = {}
        for i in magazine:
            if i not in hashmap:
                hashmap[i] = 1
            else:
                hashmap[i] += 1
        
        for i in ransomNote:
            if i not in magazine:
                return False
            if hashmap[i] > 0:
                hashmap[i] -= 1
            else:
                return False
            
        return True