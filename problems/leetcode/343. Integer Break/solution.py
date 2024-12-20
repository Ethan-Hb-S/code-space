#
class Solution:
    def integerBreak(self, n: int) -> int:
        # Consider Euler's Number (e)
        if n == 2:
            return 1
        elif n == 3:
            return 2
        else:
            if not n % 3:
                return 3 ** (n // 3)
            elif n % 3 == 1:
                return 3 ** (n // 3 - 1) * 4
            else:
                return 3 ** (n // 3) * 2
                