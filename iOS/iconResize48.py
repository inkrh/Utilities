#!/usr/bin/python

from PIL import Image
from resizeimage import resizeimage
import sys
import os

size = 48

def resize(filename, image, x,y, ext):
    output = resizeimage.resize_cover(image, [x,y], validate=False)
#   PIL doesn't like JPG uses JPEG
#   should really filter all
    if(ext=='jpg'):
        ext='JPEG'
    
    output.save(str(filename) + "-"+str(x) + "."+ext, ext)

def runfortyeight(filename):
    global size
    with open(filename, 'r+b') as f:
        with Image.open(f) as image:
            width, height = image.size
            if width == height == 48:
                return (filename + " already 48px square")
            resize(filename[:-4],image, size,size, filename[-3:])
            return (filename + " done")

def oswalk(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            if name.lower().endswith(".png") or name.lower().endswith(".jpg") or name.lower().endswith(".jpeg"):
                print(runfortyeight(os.path.join(root, name)))


#oswalk("filename") - use "__main__" to do so
if __name__ == '__main__':
    try:
        oswalk(sys.argv[1])
    except:
        print("resize failed")
