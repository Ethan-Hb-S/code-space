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
    public int sumOfLeftLeaves(TreeNode root) {
        int[] ans = {0};

        this.recursion(root, false, ans);

        return ans[0];
    }

    private void recursion(TreeNode node, boolean isLeft, int[] ans) {
        if (node.left == null && node.right == null) {
            if (isLeft) {
                ans[0] += node.val;
            } else {
                return;
            }
        }

        if (node.left != null) this.recursion(node.left, true, ans);
        if (node.right != null) this.recursion(node.right, false, ans);
    }
}