#
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        if obstacleGrid[0][0]: return 0
        y, x = len(obstacleGrid), len(obstacleGrid[0])
        dp = [[ 0 for _ in range(x) ] for _ in range(y)]

        for i in range(y):
            if obstacleGrid[i][0]:
                break
            dp[i][0] = 1
        for i in range(x):
            if obstacleGrid[0][i]:
                break
            dp[0][i] = 1

        for j in range(1, y):
            for i in range(1, x):
                if not obstacleGrid[j][i]:
                    dp[j][i] = dp[j-1][i] + dp[j][i-1]

        return dp[-1][-1]
