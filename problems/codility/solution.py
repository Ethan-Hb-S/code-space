import json

# Overall Time Complexity:
# Overall Space Complexity:
def solution(name, age):
    return 

if __name__ == '__init__':
    print()

with open('test-input.txt', 'r') as f:
    json_str = ''.join(f.readlines())
    data = json.loads(json_str)
    for i in data:
        print(solution(i['name'], i['age']))

import numpy as np

# 生成10百万个随机整数
random_data = np.random.randint(1, 10**6, size=10000000)