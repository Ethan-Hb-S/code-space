#
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        self.traverse(root, res)
        return res
        
    def traverse(self, node, arr):
        if not node: return

        self.traverse(node.left, arr)
        arr.append(node.val)
        self.traverse(node.right, arr)