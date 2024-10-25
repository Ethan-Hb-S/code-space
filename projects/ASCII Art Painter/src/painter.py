import sys, random, argparse
from PIL import Image
import numpy as np
import math

# Character ramps below referred from Paul Bourke's <<Character representation of grey scale images>>
# 70 levels of gray
GSCALE_70 = '''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''

# 10 levels of gray
GSCALE_10 = " .:-=+*#%@"

# default number of columns
COL_DEFAULT = 100

# default width-height ratio of font as using Courier
RATIO_DEFAULT = 0.43

def func(filename, cols=COL_DEFAULT, ratio=RATIO_DEFAULT):
    img = Image.open(filename).convert('L')
    # img.size[0]/img.size[1] will do the same
    width, height = img.width, img.height
    w = width / cols
    h = w / ratio
    rows = int(height / h)


def getAverageL(image):
    matrix = np.array(image)
    w, h = matrix.shape
    seq = matrix.reshape(w * h)
    return np.mean(seq)
