#!/usr/bin/python

from PIL import Image
from resizeimage import resizeimage
import sys

sizes = [29,40,50,57,58,72,76,80,87,100,114,120,144,152,167,180,512,1024]

def resize(filename, image, x,y):
    output = resizeimage.resize_cover(image, [x,y], validate=False)
    output.save(str(filename) + str(x)+"x" + str(y) + ".png", "PNG")


def iterateSizes(filename):
    global sizes
    with open(filename, 'r+b') as f:
        with Image.open(f) as image:
            width, height = image.size
                            
            if  width == height:
                if width < 1024 or height < 1024:
                    print("warning: low resolution source")
                    
                try:
                    for i in sizes:
                        resize(filename[:-4], image,i,i)
                    return(filename + " done")
                except:
                    return(filename + " failed\n" + str(sys.exc_info()[0]))
            else:
                    return(filename + " is not square")
    


if __name__ == '__main__':
    try:
        print(iterateSizes(sys.argv[1]))
    except:
        print("resize failed")
