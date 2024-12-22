#
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        self.traverse(root)
        return root
        
    def traverse(self, node):
        if not node: return
        node.left, node.right = node.right, node.left
        self.traverse(node.left)
        self.traverse(node.right)