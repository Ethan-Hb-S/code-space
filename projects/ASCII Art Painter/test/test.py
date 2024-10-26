import os, subprocess

# locate folder for testing
DIR_TEST_IN = 'img/'
MAIN = '../src/painter.py'

files = os.listdir(DIR_TEST_IN)

for f in files:
    path = os.path.join(f)
    subprocess.run(['python', MAIN, '-f', path, '-t'])