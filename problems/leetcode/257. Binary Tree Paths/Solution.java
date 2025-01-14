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
    public List<String> binaryTreePaths(TreeNode root) {
        List<String> res = new ArrayList<>();
        
        recursion(root, "", res);

        return res;
    }

    private void recursion(TreeNode node, String path, List<String> list) {
        path += Integer.toString(node.val);
        if (node.left == null && node.right == null) {
            list.add(path);
        } else {
            path += "->";
        }

        if (node.left != null) {
            this.recursion(node.left, path, list);
        }
        if (node.right != null) {
            this.recursion(node.right, path, list);
        }
    }
}