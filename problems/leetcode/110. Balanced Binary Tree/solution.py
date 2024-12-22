#
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def traverse(node, depth):
            if not node: return depth - 1
            l = traverse(node.left, depth + 1)
            r = traverse(node.right, depth + 1)
            return -1 if abs(l - r) > 1 else max(l, r)

        return traverse(root, 1) > 0 if root else True