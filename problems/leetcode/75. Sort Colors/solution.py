# 2 pointers swap approach
# class Solution:
#     def sortColors(self, nums: List[int]) -> None:
#         """
#         Do not return anything, modify nums in-place instead.
#         """
#         self.quickSort(nums, 0, len(nums))

#     def quickSort(self, nums, low, upp):
#         if low >= upp-1: return
#         pivot = nums[low]
#         left, right = low, upp-1
#         curr = 0

#         while left < right:
#             while nums[left] <= pivot:
#                 if left >= right: break
#                 left += 1
            
#             while nums[right] >= pivot:
#                 if left >= right: break
#                 right -= 1

#             if left >= right:
#                 curr = (left-1) if nums[left] >= pivot else left
#                 nums[curr], nums[low] = nums[low], nums[curr]
#             else:
#                 nums[left], nums[right] = nums[right], nums[left]

#         self.quickSort(nums, low, curr)
#         self.quickSort(nums, curr+1, upp)


# 3 pointers approach
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        