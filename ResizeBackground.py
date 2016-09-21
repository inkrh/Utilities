from PIL import Image
from resizeimage import resizeimage


sizes= [(640,1136),(750,1334),(1242,2208),(1536,2048),(2048,2732)]


def resize(filename, image, x,y):
    output = resizeimage.resize_cover(image, [x,y], validate=False)
    print(filename)
    output.save(filename, "PNG")


def Process(file):
    i = Image.open(file)
    for x,y in sizes:
        #portrait
        resize(file.replace('.png','p'+str(x)+'_'+str(y)+'.png'),i,x,y)
        #landscape
        resize(file.replace('.png','l'+str(y)+'_'+str(x)+'.png'),i,y,x)
        
        
    
