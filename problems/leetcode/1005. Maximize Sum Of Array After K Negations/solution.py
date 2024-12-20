#
class Solution:
    def largestSumAfterKNegations(self, nums: List[int], k: int) -> int:
        arr = sorted(nums)
        i, t = 0, 0
        total = sum(arr)
        mini = arr[i]

        while t < k:
            mini *= -1
            total += mini * 2
            if i+1 < len(arr) and mini > arr[i+1]:
                mini = arr[i+1]
                i += 1
            t += 1

        return total