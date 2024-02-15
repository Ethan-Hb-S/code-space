class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        new = [0] * (m + n)
        
        curr = 0
        i, j = 0, 0
        while curr < m + n:
            if i < m:
                n1 = nums1[i]
            else:
                n1 = float('inf')

            if j < n:
                n2 = nums2[j]
            else:
                n2 = float('inf')
            
            if n1 < n2:
                new[curr] = nums1[i]
                i += 1
            else:
                new[curr] = nums2[j]
                j += 1

            curr += 1

        for t in range(m+n):
            nums1[t] = new[t]