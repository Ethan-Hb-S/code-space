#
from collections import deque 
class MyStack:

    def __init__(self):
        self.qin = deque()
        self.qout = deque()

    def push(self, x: int) -> None:
        if self.qout:
            self.qin.append(self.qout.pop())
        self.qout.append(x)

    def pop(self) -> int:
        if not len(self.qout):
            if len(self.qin):
                for i in range(len(self.qin)):
                    self.qout.append(self.qin.popleft())
                for i in range(len(self.qout)-1):
                    self.qin.append(self.qout.popleft())
            else:
                return None
            
        return self.qout.pop()

    def top(self) -> int:
        value = self.pop()
        self.qout.append(value)
        return value

    def empty(self) -> bool:
        return (not self.qin and not self.qout)


# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()