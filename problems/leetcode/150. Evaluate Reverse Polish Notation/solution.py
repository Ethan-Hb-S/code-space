#
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        table = set(['*', '/', '+', '-'])

        for i in tokens:
            if i in table and len(stack) > 1:
                b, a = stack.pop(), stack.pop()
                if i == '*':
                    stack.append(a*b)
                if i == '/':
                    stack.append(int(a/b))
                if i == '+':
                    stack.append(a+b)
                if i == '-':
                    stack.append(a-b)
            else:
                stack.append(int(i))
        
        return stack[0]