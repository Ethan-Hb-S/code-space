# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(K, A):
    # Implement your solution here
    total = 0
    length = 0
    
    for i in A:
        length += i
        if length >= K:
            total += 1
            length = 0
            
    return total