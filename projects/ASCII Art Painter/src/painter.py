import sys, argparse
from PIL import Image
import numpy as np

# Character ramps below referred from Paul Bourke's <<Character representation of grey scale images>>
# 70 levels of gray
GSCALE_70 = '''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''

# 16 levels of gray
GSCALE_16 = "@%8#Z0oc?*+=:^'. "

# 10 levels of gray
GSCALE_10 = "@%#*+=-:. "

# default number of columns (equivalent to resolution)
COL_DEFAULT = 1200

# default width-height ratio of font as using Courier
RATIO_DEFAULT = 0.43

# locate folder for testing
DIR_TEST_IN = '../test/img/'
DIR_TEST_OUT = '../test/output/'

def convertToASCII(filename, cols, ratio, moreLevels):
    '''
    Given image file, returns ASCII graphics
    '''
    img = Image.open(filename).convert('L')
    # img.size[0]/img.size[1] will do the same
    width, height = img.width, img.height

    # w represents a single tile's unit width, h represents the its unit height
    w = width / cols
    h = w / ratio
    rows = int(height / h)
    print(rows)
    res = []

    # set up vertical bounds for each tile
    for r in range(rows):
        y0 = int(r * h)
        y1 = int(r * h + h) if int(r * h + h) > y0 else y0+1
        if r == rows - 1:
            y1 = height
        
        # set up horizontal bounds for each tile
        for c in range(cols):
            x0 = int(c * w)
            x1 = int(c * w + w) if int(c * w + w) > x0 else x0+1
            if c == cols - 1:
                x1 = width

            # calculate average luminance of the tile and then match it with greyscale
            i = img.crop((x0, y0, x1, y1))
            gmean = int(getAverageL(i))
            if moreLevels:
                char = GSCALE_16[int(gmean / 255 * 16)]
            else:
                char = GSCALE_10[int(gmean / 255 * 9)]
            res.append(char)
        
        res.append('\n')
    return ''.join(res)

def getAverageL(image):
    '''
    Given PIL Image object, returns average value of luminance
    '''
    matrix = np.array(image)
    w, h = matrix.shape
    return np.mean(matrix.reshape(w * h))

def changeSuffix(file:str, suffix:str):
    flist = file.split('.')
    flist[-1] = suffix
    return '.'.join(flist)

def main():
    parser = argparse.ArgumentParser(description='Process image to ASCII graphics')
    parser.add_argument('-f', '--filename', type=str, required=True, help="Target file's name and location")
    parser.add_argument('-c', '--columns', type=int, dest='cols', help='Expected number of tile columns')
    parser.add_argument('-r', '--ratio', type=float, help='Expected ratio(scale) of font width and height')
    parser.add_argument('-l', '--moreLevels', action='store_true', help='If apply higher levels of greyscales, 10 levels if true, 16 otherwise')
    parser.add_argument('-o', '--outfile', type=str, dest='output', help='Expected output file name')
    parser.add_argument('-t', '--test', action='store_true', help='If this is test mode')

    args = parser.parse_args()
    fname:str = args.filename
    if args.test:
        fname = DIR_TEST_IN + fname
        
    if args.output:
        outname = args.output
    else:
        outname = fname.split('/')[-1]
    
    cols = args.cols if args.cols else COL_DEFAULT
    ratio = args.ratio if args.ratio else RATIO_DEFAULT
    moreLevels = True if args.moreLevels else False
    res = convertToASCII(fname, cols, ratio, moreLevels)

    addr = DIR_TEST_OUT if args.test else ''
    addr += outname
    addr = changeSuffix(addr, 'txt')

    outfile = open(addr, mode='w')
    outfile.write(res)
    outfile.close
    print('ASCII art completed on ->' + addr)

if __name__ == '__main__':
    main()
