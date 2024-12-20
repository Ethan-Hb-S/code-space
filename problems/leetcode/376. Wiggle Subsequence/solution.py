#
class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:
        if len(nums) < 2: return 1
        diff = []
        res = 1

        for i in range(1, len(nums)):
            d = nums[i] - nums[i-1]
            if d:
                diff.append(d)

        if len(diff):
            prev = -diff[0]
            for i in diff:
                if prev * i < 0:
                    res += 1
                    prev = i

        return res
