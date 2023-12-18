#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'minimumBribes' function below.
#
# The function accepts INTEGER_ARRAY q as parameter.
#

def minimumBribes(q):
    # Write your code here
    n = len(q)-1
    d = {}
    sortQ = sorted(q)
    if q == sortQ:
        return 0
        
    left, right = 0, n
    while q != sortQ:
        for i in range(left, right):
            if q[i] > q[i+1]:
                if q[i] in d:
                    d[q[i]] += 1
                else:
                    d[q[i]] = 1
                q[i], q[i+1] = q[i+1], q[i]
    
    values = d.values()
    for v in values:
        if v > 2:
            print('Too chaotic')
            return
    print(sum(values))
        
    

if __name__ == '__main__':
    t = int(input().strip())

    for t_itr in range(t):
        n = int(input().strip())

        q = list(map(int, input().rstrip().split()))

        minimumBribes(q)
    
