import os
from PIL import Image

def ConvertPNGtoTIFF(path):
    for root,subdirs,files in os.walk(path):
        
        for f in files:
            
            fp = os.path.join(root,f)
            if ".png" in fp:
                newName = fp.replace(".png",".tiff")
                i = Image.open(fp)
                i.save(newName,"TIFF")
