#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'legoBlocks' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER height
#  2. INTEGER width
#

def legoBlocks(height, width):
    # all below present variations
    row = [1]
    col = [1]
    all = [1]
    
    for i in range(1, width + 1):
        sumhg = 0
        for j in range(1, i):
            sumhg += all[j] * col[i-j] % (10**9+7)
        
        # each row has total variations as the sum of last 4 width's variations
        row.append(sum(row[-4:]) % (10**9+7))

        # each column has total variations as the result of variations of the row to the power of height
        col.append(row[i] ** height % (10**9+7))
        
        all.append((col[i] - sumhg) % (10**9+7))

    return all[-1] % (10**9+7)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(input().strip())

    for t_itr in range(t):
        first_multiple_input = input().rstrip().split()

        n = int(first_multiple_input[0])

        m = int(first_multiple_input[1])

        result = legoBlocks(n, m)

        fptr.write(str(result) + '\n')

    fptr.close()
