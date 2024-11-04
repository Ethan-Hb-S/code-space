
def kmp(string, sub) -> int:
    table = build_table(sub)
    i, j = 0, 0

    while i < len(string):
        if string[i] == sub[j]:             # if this char matches
            i += 1
            j += 1
        elif j > 0:                         # if not but some of them matched
            j = table[j - 1]
        else:                               # if the beginning char dont even match
            i += 1
        
        if j == len(sub):                   # return the start index of substring when fully matched
            return i - j
    return -1

def build_table(sub) -> list:
    length = len(sub)
    table = [0] * length
    prefix = 0

    for i in range(1, length):
        if sub[i] == sub[prefix]:
            prefix += 1
            table[i] = prefix
        else:
            prefix = 0

    return table