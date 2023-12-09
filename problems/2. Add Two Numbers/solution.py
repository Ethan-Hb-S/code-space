# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        d1 = {}
        d2 = {}

        # use dictionary to store the indices and values
        node: ListNode = l1
        index = 0
        while node != None:
            d1[index] = node.val
            node = node.next
            index += 1

        node: ListNode = l2
        index = 0
        while node != None:
            d2[index] = node.val
            node = node.next
            index += 1
        
        length = max(len(d1.keys()), len(d2.keys()))

        start: ListNode = ListNode()
        prev: ListNode = ListNode()
        carry = 0
        for i in range(length):
            v1 = d1[i] if i in d1 else 0
            v2 = d2[i] if i in d2 else 0
            res = v1 + v2 + carry
            '''
            carry = 0
            if res > 9:
                carry = 1
                res -= 10
            '''
            carry = res // 10
            
            node = ListNode(res % 10, None)
            if i > 0:
                prev.next = node
            else:
                start.next = node
            prev = node
            
            if i + 1 == length and carry == 1:
                node.next = ListNode(carry, None)
        return start.next