class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        l = len(prices)

        profit = [ [0] * 2 ] * (l+1)
        profit[0][1] = float('-inf')

        for i in range(1, l+1):
            profit[i][0] = max(profit[i-1][0], profit[i-1][1] + prices[i-1])
            profit[i][1] = max(profit[i-1][1], profit[i-1][0] - prices[i-1])
        
        print(profit)
        return profit[l][0]
    
        '''
        def dfs(d, hold):
            if d == 0:
                return 0 if not hold else float('-inf')

            if hold:
                return max(dfs(d-1, True), dfs(d-1, False) - prices[d-1])
            return max(dfs(d-1, False), dfs(d-1, True) + prices[d-1])
        
        return dfs(l, False)
        '''