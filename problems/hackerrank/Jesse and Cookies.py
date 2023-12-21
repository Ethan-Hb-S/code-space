#!/bin/python3

import math
import os
import random
import re
import sys
import heapq

#
# Complete the 'cookies' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER k
#  2. INTEGER_ARRAY A
#

def cookies(k, A):
    # Write your code here
    heapq.heapify(A)
    total = 0
    min = heapq.heappop(A)
    while min < k:
        second = heapq.heappop(A)
        value = min + 2 * second
        heapq.heappush(A, value)
        min = heapq.heappop(A)
        total += 1
        if len(A) == 0:
            break
    
    if min < k:
        return -1
    return total
    
def binarySearch(arr, n):
    min, max = 0, len(arr)-1
    while min < max:
        mid = (min + max + 1) // 2
        # print(f'{min} {max}')
        if arr[mid] < n:
            max = mid - 1
        elif arr[mid] > n:
            min = mid + 1
        else:
            return mid
    return min

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    k = int(first_multiple_input[1])

    A = list(map(int, input().rstrip().split()))

    result = cookies(k, A)

    fptr.write(str(result) + '\n')

    fptr.close()
