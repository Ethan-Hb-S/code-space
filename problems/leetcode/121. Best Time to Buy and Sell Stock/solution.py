class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if is_decreasing(prices):
            return 0

        maximums = [0] * len(prices)
        maximums[-1] = prices[-1]
        i = len(prices) - 2
        pro = 0
        while i >= 0:
            maximums[i] = max(maximums[i+1], prices[i+1])
            if maximums[i] > prices[i]:
                pro = max(pro, (maximums[i] - prices[i]))
            i -= 1
        
        return pro

def is_decreasing(l: list):
    prev = l[0]
    for i in l[1:]:
        if i > prev:
            return False
        prev = i
    return True