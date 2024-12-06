import urllib.request as ur
import re

def decode(url: str):
    res = ur.urlopen(url).read()
    data = res.decode('utf-8')
    pattern = r'<tr.*?>.*?<td.*?>.*?<span.*?>(\d+)</span>.*?</td>.*?<td.*?>.*?<span.*?>([\u2580-\u25FF])</span>.*?</td>.*?<td.*?>.*?<span.*?>(\d+)</span>.*?</td>.*?</tr>'
    matches = re.findall(pattern, data)

    grad = {}
    rangeX, rangeY = 0, 0
    for i in matches:
        x, pos, y = i
        x, y = int(x), int(y)
        if x > rangeX:
            rangeX = x
        if y > rangeY:
            rangeY = y

        if y in grad:
            grad[y][x] = pos
        else:
            grad[y] = {
                x: pos
            }
    
    for j in range(rangeY, -1, -1):
        if j not in grad:
            print(' ' * rangeX)
        else:
            for i in range(rangeX+1):
                if i in grad[j]:
                    print(grad[j][i], end='')
                else:
                    print(' ', end='')
            print()


if __name__ == '__main__':
    test = 'https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub'
    url = 'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub'
    decode(url)

'''
<tr class="c2">
<td class="c0" colspan="1" rowspan="1"><p class="c1"><span class="c3">42</span></p></td>
<td class="c4" colspan="1" rowspan="1"><p class="c1"><span class="c3">█</span></p></td>
<td class="c0" colspan="1" rowspan="1"><p class="c1"><span class="c3">6</span></p></td>
</tr>
'''