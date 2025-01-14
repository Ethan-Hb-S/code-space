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
    public TreeNode constructMaximumBinaryTree(int[] nums) {
        TreeNode root = new TreeNode();
        this.recursion(nums, 0, nums.length, root);
        return root;
    }

    private void recursion(int[] nums, int start, int end, TreeNode node) {
        if (start >= end) return;
        int max = start;
        for (int i = start + 1; i < end; i++) {
            max = (nums[i] > nums[max]) ? i : max;
        }
        
        node.val = nums[max];
        if (start < max) {
            node.left = new TreeNode();
            this.recursion(nums, start, max, node.left);
        }
        if (max + 1 < end) {
            node.right = new TreeNode();
            this.recursion(nums, max + 1, end, node.right);
        }
    }
}