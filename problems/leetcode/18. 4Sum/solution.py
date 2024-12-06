#
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        l = len(nums)
        snums = sorted(nums)
        ans = []
        table = set([])

        for j in range(l-3):
            notFound = True
            for i in range(j+1, l-2, 1):
                left, right = i+1, l-1

                while left < right:
                    c = (snums[i], snums[j], snums[left], snums[right])
                    dif = snums[i] + snums[j] + snums[left] + snums[right] - target
                    if not dif:
                        if hash(c) not in table:
                            notFound = False
                            ans.append([snums[i], snums[j], snums[left], snums[right]])
                            table.add(hash(c))
                            right -= 1
                        left += 1
                    elif dif > 0:
                        right -= 1
                    else:
                        left += 1
                
                if notFound and sum(snums[j:j+4]) > target:     # sum() here can be optimized by simply do addition
                    return ans
        return ans