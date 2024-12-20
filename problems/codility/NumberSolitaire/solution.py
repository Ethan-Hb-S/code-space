# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(A):
    end = len(A) - 1
    dp = [0] * (len(A))
    dp[0] = A[0]
    
    for i in range(1, end + 1):
        max_val = max(dp[max(0, i - 6):i])
        dp[i] = max_val + A[i]
    
    return dp[end]