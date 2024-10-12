# Hashtable method
# class Solution:
#     def threeSum(self, nums: List[int]) -> List[List[int]]:
#         res = set()
#         d = set()

#         for i in range(len(nums)):
#             d.clear()
#             x = nums[i]
#             for y in nums[i+1:]:
#                 z = -x - y
#                 if y in d:
#                     res.add(tuple(sorted([x, y, z])))
#                 d.add(z)
        
#         ans = []
#         for i in res:
#             ans.append(i)
#         return ans


# Double pointers method
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        arr = sorted(nums)
        ans = []
        xprev = None
        
        for i in range(len(arr)):
            x = arr[i]
            left, right = i+1, len(arr)-1
            yprev, zprev = None, None

            while left < right and x != xprev:
                y, z = arr[left], arr[right]
                dif = x + y + z
                if y != yprev or z != zprev:
                    if dif == 0:
                        ans.append([x, y, z])
                        yprev = y
                        zprev = z
                if y == yprev and z == zprev:
                    left += 1
                    right -= 1
                    continue

                if dif < 0:
                    left += 1
                if dif > 0:
                    right -= 1

            xprev = x

        return ans