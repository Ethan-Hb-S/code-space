/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public boolean hasPathSum(TreeNode root, int targetSum) {
        boolean ans = recursion(root, targetSum);

        return ans;
    }

    private boolean recursion(TreeNode node, int diff) {
        if (node == null) return false;
        if (node.left == null && node.right == null && node.val == diff) {
            return true;
        }

        return recursion(node.left, diff - node.val) || recursion(node.right, diff - node.val);
    }
}