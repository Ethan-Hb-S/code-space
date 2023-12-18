class Solution:
    def largestGoodInteger(self, num: str) -> str:
        ans = ''
        prev2, prev1 = num[0], num[1]
        for c in num[2:]:
            #if prev1 == prev2 and prev1 == c:
            if prev2 == prev1 == c:
                if ans == '' or ans[0] < c:
                    ans = ''.join([c * 3])
                    
            prev2 = prev1
            prev1 = c
        return ans