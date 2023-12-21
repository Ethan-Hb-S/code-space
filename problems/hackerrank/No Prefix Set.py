#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'noPrefix' function below.
#
# The function accepts STRING_ARRAY words as parameter.
#

def addToTree(tree, word):
    if len(word) == 0:
        return tree
    
    l = word[0]
    if l in tree:
        tree[l] = addToTree(tree[l], word[1:])
    else:
        tree[l] = addToTree(dict(), word[1:])
    
    return tree

def checkInTree(tree, word):
    if len(word) == 0:
        return True
    if len(tree) == 0:
        return True
        
    l = word[0]
    if l not in tree:
        return False
    return checkInTree(tree[l], word[1:])
    

def noPrefix(words):
    tree = dict()
    inTree = False
    for w in words:
        if len(tree) != 0:
            inTree = checkInTree(tree, w)
        if inTree:
            print("BAD SET")
            print(w)
            return
        tree = addToTree(tree, w)
    print("GOOD SET")

if __name__ == '__main__':
    n = int(input().strip())

    words = []

    for _ in range(n):
        words_item = input()
        words.append(words_item)

    noPrefix(words)
