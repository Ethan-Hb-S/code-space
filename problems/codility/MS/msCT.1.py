# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(buckets):
    # Implement your solution here
    table = {}
    for i in range(len(buckets)):
        if buckets[i] == 'B': 
            table.setdefault(i, buckets[i])
    
    if len(table) > (len(buckets) + 1) // 2:
        return -1
    
    curr = 0
    mini_even = len(table) - 1
    mini_odd = float('inf') if len(table) * 2 + 1 >= len(buckets) else len(table)
    while curr < len(buckets):
        # for buckets of even indice
        if curr in table and (curr - 2) in table:
            mini_even -= 1

        # for buckets of odd indice
        if (curr + 1) < len(buckets) and (curr + 1) in table and (curr - 1) in table:
            mini_odd -= 1

        curr += 2
    
    return min(mini_even, mini_odd)


print(solution(['B']) == 0)
print(solution(['B', '.', 'B', '.','B']) == 0)
print(solution(['B', 'B', '.',  '.','B']))
print(solution(['B', '.', '.', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.','B']) == 2)