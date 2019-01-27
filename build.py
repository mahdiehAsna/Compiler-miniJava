import sys
from os import listdir
import subprocess

subprocess.call('python main.py ' + sys.argv[1], shell=True)

jasmins = listdir('intermediateCode')

for j in jasmins:
    subprocess.call('jasmin -d output intermediateCode/' + j, shell=True)

print()
