#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'truckTour' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY petrolpumps as parameter.
#

def truckTour(petrolpumps):
    # Write your code here
    d = {}
    length = len(petrolpumps)
    for p in range(length):
        d[p] = (petrolpumps[p][0], petrolpumps[p][1])
    
    for p in range(length):
        tank = 0
        breaked = False
        
        for i in range(p, length):
            tank += d[i][0]
            if tank < d[i][1]:
                breaked = True
                break
            else:
                tank -= d[i][1]
        
        if not breaked:
            for i in range(0, p):
                tank += d[i][0]
                if tank < d[i][1]:
                    breaked = True
                    break
                else:
                    tank -= d[i][1]
        
        if breaked:
            continue
        return p

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    petrolpumps = []

    for _ in range(n):
        petrolpumps.append(list(map(int, input().rstrip().split())))

    result = truckTour(petrolpumps)

    fptr.write(str(result) + '\n')

    fptr.close()
