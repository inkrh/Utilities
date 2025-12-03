from PIL import Image
import sys, os

def saveAsPNG(filename):
    pngName = filename.lower().replace('.jpg','.png').replace('.jpeg','.png')
    with open(filename, 'r+b') as f:
        with Image.open(f) as image:
            image.save(str(pngName),"PNG")


def oswalk(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            if name.lower().endswith(".png") or name.lower().endswith(".jpg") or name.lower().endswith(".jpeg"):
                saveAsPNG(os.path.join(root, name))


#oswalk("filename") - use "__main__" to do so
if __name__ == '__main__':
    try:
        oswalk(sys.argv[1])
    except:
        print("Convert failed")
