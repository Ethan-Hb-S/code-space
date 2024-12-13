import heapq
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        table = {}
        res = []

        for i in nums:
            if i not in table:
                table[i] = 1
            else:
                table[i] += 1
        
        for i,j in table.items():
            heapq.heappush(res, (j, i))
            if len(res) > k:
                heapq.heappop(res)

        ans = [0] * k
        for i in range(len(res)-1, -1, -1):
            ans[i - k + 1] = res[i][1]

        return ans