#
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        table = {
            ')': '(',
            ']': '[',
            '}': '{'
        }
        
        for i in s:
            if len(stack) and i in table and stack[-1] == table[i]:
                stack.pop()
            else:
                stack.append(i)
        
        return (not len(stack))