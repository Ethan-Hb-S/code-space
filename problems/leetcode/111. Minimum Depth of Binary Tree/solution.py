#
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        def traverse(node, depth):
            if not node: return float('inf')
            if not node.left and not node.right: return depth
            return min(traverse(node.left, depth + 1), traverse(node.right, depth + 1))

        return traverse(root, 1) if root else 0