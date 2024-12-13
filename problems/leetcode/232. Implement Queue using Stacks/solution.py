#
class MyQueue:

    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def push(self, x: int) -> None:
        self.stack_in.append(x)

    def pop(self) -> int:
        if not self.stack_out:
            if self.stack_in:
                while self.stack_in:
                    self.stack_out.append(self.stack_in.pop())
            else:
                return None
        return self.stack_out.pop()
        
    def peek(self) -> int:
        if self.stack_out:
            return self.stack_out[-1]
        elif self.stack_in:
            return self.stack_in[0]
        else:
            return None

    def empty(self) -> bool:
        return (not self.stack_in and not self.stack_out)


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()