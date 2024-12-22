# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root: return []
        q = deque()
        q.append(root)
        res = []
        k = 1

        while len(q):
            arr = []
            n = 0
            for _ in range(k):
                if not len(q): break
                node = q.popleft()
                n += self.traverse(node, q)
                arr.append(node.val)
            k = n
            res.append(arr)

        return res
        
    def traverse(self, node, queue):
        if not node: return
        n = 0
        if node.left:
            n += 1
            queue.append(node.left)
        if node.right:
            n += 1
            queue.append(node.right)
        return n