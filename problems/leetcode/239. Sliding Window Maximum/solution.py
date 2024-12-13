#
from collections import deque
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        q = MonoQueue()
        res = [0] * (len(nums) - k + 1)
        
        for i in range(len(nums)):
            if i >= k:
                q.pop(nums[i - k])

            q.push(nums[i])
            if i >= k-1:
                res[i - k + 1] = q.getMax()
        
        return res


class MonoQueue:
    def __init__(self):
        self.q = deque()
    
    def push(self, value):
        # print(f'{self.q} + {value}')
        while self.q and value > self.q[-1]:
            self.q.pop()
        self.q.append(value)

    def pop(self, value):
        if self.getMax() == value:
            self.q.popleft()

    def getMax(self):
        return self.q[0]