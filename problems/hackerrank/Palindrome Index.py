#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'palindromeIndex' function below.
#
# The function is expected to return an INTEGER.
# The function accepts STRING s as parameter.
#

def palindromeIndex(s):
    # Write your code here
    if check(s):
        return -1
    length = len(s)
    for i in range(length // 2):
        if s[i] != s[length - i - 1]:
            if check(s[:i] + s[i+1:]):
                return i
            elif check(s[:length - i - 1] + s[length - i:]):
                return length - i - 1
    return -1
    
def check(s):
    return s == s[::-1]

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input().strip())

    for q_itr in range(q):
        s = input()

        result = palindromeIndex(s)

        fptr.write(str(result) + '\n')

    fptr.close()
