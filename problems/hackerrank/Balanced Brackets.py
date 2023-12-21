#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'isBalanced' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
    
    def push(self, value):
        new = Node(value)
        if self.top is not None:
            new.next = self.top
        self.top = new
    
    def pop(self):
        value = self.top.value
        self.top = self.top.next
        return value
    
    def show(self):
        if not self.top:
            return None
        return self.top.value

def isBalanced(s):
    # Write your code here
    stack = Stack()
    for i in s:
        if i == '{' or i == '[' or i == '(':
            stack.push(i)
        else:
            sign = stack.show()
            if (sign == '{' and i == '}') or (sign == '[' and i == ']') or (sign == '(' and i == ')'):
                stack.pop()
            else:
                return 'NO'
    
    if not stack.show():
        return 'YES'
    return 'NO'

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(input().strip())

    for t_itr in range(t):
        s = input()

        result = isBalanced(s)

        fptr.write(result + '\n')

    fptr.close()
