from PIL import Image
from resizeimage import resizeimage


sizes= [(640,960),(640,1136),(750,1334),(1242,2208),(768,1024),(2048,2732)]



names = ["@2x~iphone","-568@2x~iphone","-667@2x~iphone","-736@3x~iphone","~ipad","-1366@2x~ipad"]

def pl(x,y):
    if x > y:
        return "-Landscape"
    return "-Portrait"


def resize(filename, image, x,y):
    output = resizeimage.resize_cover(image, [x,y], validate=False)
    print(filename)
    output.save(filename, "PNG")


def Process(file):
    i = Image.open(file)
    c = 0
    for x,y in sizes:
        #portrait
        resize(file.replace('.png',pl(x,y)+names[c]+'.png'),i,x,y)
        #landscape
        resize(file.replace('.png',pl(y,x)+names[c]+'.png'),i,y,x)
        c += 1
        
        
    
