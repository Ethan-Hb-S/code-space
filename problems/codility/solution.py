import json

def solution(name, age):
    return f'{name}: {age}'

if __name__ == '__init__':
    print('hei')

with open('test-input.txt', 'r') as f:
    json_str = ''.join(f.readlines())
    data = json.loads(json_str)
    for i in data:
        print(solution(i['name'], i['age']))