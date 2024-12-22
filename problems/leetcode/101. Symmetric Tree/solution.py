#
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        q = deque()
                   
        def traverseLeft(node):
            if not node: 
                q.appendleft(None)
            else:
                q.appendleft(node.val)
                traverseLeft(node.left)
                traverseLeft(node.right)

        def traverseRight(node):
            if not node: 
                q.append(None)
            else:
                q.append(node.val)
                traverseRight(node.right)
                traverseRight(node.left)
            
        traverseLeft(root.left)
        traverseRight(root.right)
        while len(q):
            if q.pop() != q.popleft():
                return False
        
        return True