import math

def solution(A):
    # Implement your solution here
    if not len(A): return []
    value = math.ceil(binToDec(A) / 2)
    return decToBin(value)

def binToDec(A: list):
    res = 0
    power = 0
    
    for i in A:
        res += i * (-2) ** power
        power += 1

    return res

def decToBin(value: int):
    arr = []

    while value:
        remind = value % (-2)
        value /= 2

        if remind < 0:
            remind -= -2
            value += 1

        arr.append(remind)
        if abs(value) < 1: break

    return arr