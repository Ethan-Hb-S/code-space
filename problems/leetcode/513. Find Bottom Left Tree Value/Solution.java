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
    public int findBottomLeftValue(TreeNode root) {
        Wrapper ans = new Wrapper();

        recursion(root, 1, ans);

        return ans.value;
    }

    private void recursion(TreeNode node, int depth, Wrapper ans) {
        if (node.left == null && node.right == null && ans.depth < depth) {
            ans.depth = depth;
            ans.value = node.val;
        }

        if (node.left != null) this.recursion(node.left, depth+1, ans);
        if (node.right != null) this.recursion(node.right, depth+1, ans);
    }
}

class Wrapper {
    int depth = 0;
    int value;
}