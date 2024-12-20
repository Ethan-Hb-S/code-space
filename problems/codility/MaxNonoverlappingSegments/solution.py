# Overall Time Complexity:
# Overall Space Complexity:
def solution(A, B):
    count = [0]
    
    for i in range(1, len(B)):
        if not overlapped(count[-1], i, A, B):
            count.append(i)
    
    return len(count)
    
def overlapped(a, b, A, B):
    return abs(A[a]-A[b]) + abs(B[a]-B[b]) <= abs(A[a]-B[a]) + abs(A[b]-B[b])
