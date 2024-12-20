# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        res = []
        self.traverse(root, targetSum, res, [])
        return res
        
    def traverse(self, root, s: int, res:list, p: list):
        if not root: return
        path = p + [root.val]
        if not root.left and not root.right and sum(path) == s:
            res.append(path)
            return
        
        if root.left:
            self.traverse(root.left, s, res, path)
        if root.right:
            self.traverse(root.right, s, res, path)