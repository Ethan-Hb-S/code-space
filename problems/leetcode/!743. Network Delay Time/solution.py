#
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        table = {}
        for i in times:
            [u, v, l] = i
            table.setdefault(u, {})[v] = l
        
        shortestPath = [ float('inf') ] * (n+1)
        shortestPath[k] = 0
        cluster = set([k])
        
        while len(cluster) < n:
            closest = None
            length = float('inf')

            for i in cluster:
                if i not in table:
                    continue
                for j in table[i]:
                    print(table[i])
                    if j not in cluster and length > table[i][j]:
                        print(j)
                        closest = j
                        length = table[i][j]
                        shortestPath[j] = min(shortestPath[j], shortestPath[i] + table[i][j])
            
            if closest: cluster.add(closest)
            print(cluster)
        
        print(shortestPath)
        return 1