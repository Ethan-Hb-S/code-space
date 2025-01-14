import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import javax.swing.tree.TreeNode;

import org.w3c.dom.ranges.Range;

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
    public TreeNode buildTree(int[] inorder, int[] postorder) {
        TreeNode root = new TreeNode();
        Map<Integer, Integer> table = new HashMap<>();
        Range rootRange = new Range(0, inorder.length, 0, postorder.length);

        for (int i = 0; i < inorder.length; i++) {
            table.put(inorder[i], i);
        }

        this.recursion(inorder, postorder, rootRange, table, root);
        return root;
    }

    private void recursion(int[] subIn, int[] subPost, Range nodeRange, Map<Integer, Integer> table, TreeNode node) {
        node.val = subPost[nodeRange.postEnd - 1];
        if (nodeRange.length <= 1) return;
        int mid = table.get(node.val);
        Range leftRange = new Range(nodeRange.inStart, mid, nodeRange.postStart, nodeRange.postStart + mid - nodeRange.inStart);
        Range rightRange = new Range(mid + 1, nodeRange.inEnd, nodeRange.postStart + mid - nodeRange.inStart, nodeRange.postEnd - 1);

        if (leftRange.length > 0) {
            node.left = new TreeNode();
            this.recursion(subIn, subPost, leftRange, table, node.left);
        }
        if (rightRange.length > 0) {
            node.right = new TreeNode();
            this.recursion(subIn, subPost, rightRange, table, node.right);
        }
    }
}

/*
class Solution {
    public TreeNode buildTree(int[] inorder, int[] postorder) {
        TreeNode root = new TreeNode();
        this.recursion(inorder, postorder, root);
        return root;
    }

    private void recursion(int[] subIn, int[] subPost, TreeNode node) {
        if (subIn.length == 0 || subPost.length == 0) return;
        int top = subPost[subPost.length - 1];
        int mid = 0;
        Set<Integer> left = new HashSet<>();

        for (int i = 0; i < subIn.length; i++) {
            if (subIn[i] == top) {
                mid = i;
                break;
            }
            left.add(subIn[i]);
        }

        int[] leftIn = Arrays.copyOfRange(subIn, 0, mid);
        int[] rightIn = Arrays.copyOfRange(subIn, mid + 1, subIn.length);

        int[] leftPost = Arrays.copyOfRange(subPost, 0, leftIn.length);
        int[] rightPost = Arrays.copyOfRange(subPost, leftIn.length, subPost.length - 1);

        node.val = top;
        if (leftIn.length > 0) {
            node.left = new TreeNode();
            this.recursion(leftIn, leftPost, node.left);
        }
        if (rightIn.length > 0) {
            node.right = new TreeNode();
            this.recursion(rightIn, rightPost, node.right);
        }
    }
}
*/