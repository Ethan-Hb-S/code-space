#
class Solution:
    def minimumTime(self, n: int, edges: List[List[int]], disappear: List[int]) -> List[int]:
        table = {}
        for i in edges:
            [a, b, l] = i
            table.setdefault(a, {})