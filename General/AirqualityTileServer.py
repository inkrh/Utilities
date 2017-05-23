import os
import sys
import io
from PIL import Image, ImageFilter
from klein import Klein
from twisted.internet import threads
import requests
import shutil
import time


##server providing blurred air quality tiles (to avoid pin style of WAQI)
##uses source tiles from waqi.info, hitting only once every 24 hours per tile to avoid
##over-using waqi.info. blurs to provide a coloured area on map


##needs simplification and style corrections
##needs time improvements - first call for a tile taking up to 8 seconds
##call once cached becomes more realistic 

##time_usage from stack overflow
def time_usage(func):
    def wrapper(*args, **kwargs):
        beg_ts = time.time()
        retval = func(*args, **kwargs)
        end_ts = time.time()
        print("elapsed time: %f" % (end_ts - beg_ts))
        return retval
    return wrapper

##if using https set your key and cert files
privateKeyPath = 'privkey.pem'
certificatePath = 'cert.pem'

##cached data folder (images from WAQI and processed images)
cachePath = 'cache/aqi/'

##WAQI token (http://waqi.info)
token = "{YOUR TOKEN}"
uri = "https://tiles.waqi.info/tiles/usepa-aqi/{z}/{x}/{y}.png?token="+token

def cacheDir(z):
    return os.path.join(cachePath,str(z))

def WAQIfilename(x, y, z):
    name= "waqi_"+str(z)+"_"+str(x)+"_"+str(y)+".png"
    return os.path.join(cacheDir(z),name)

def cacheFilename(x,y,z,):
    name = "baqi_" + str(z) + "_" + str(x) + "_" + str(y) + ".png"
    return os.path.join(cacheDir(z), name)


def WAQIgetTile(x, y, z):
    url = uri.replace('{z}',str(z)).replace('{x}',str(x)).replace('{y}',str(y))
    try:
        r = requests.get(url, stream=True)

        if r.status_code==200:
            with open(WAQIfilename(x, y, z), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw,f)

            return r.status_code, Image.open(WAQIfilename(x, y, z))
    except:
        print("Exception ", sys.exc_info()[0])

    ##any response other than 200 just return a blank image
    return r.status_code, Image.new('RGBA',(256,256),(0,0,0,0))


def fileLastModified(fn, x,y,z):
    if os.path.isfile(fn):
        stat = os.stat(fn)
        return stat.st_mtime

    return -1

def overaday(filetime):
    ##is file over 24 hours old?
    return (time.time() - filetime) > 86400

def WAQIcacheHandler(x, y, z):
    l = fileLastModified(WAQIfilename(x, y, z),x,y,z)
    ##no cached file or over 24 hours old
    if l == -1 or overaday(l):
        return WAQIgetTile(x, y, z)

    ##sanity - already covered in above, but double check there is actually a file there
    if os.path.isfile(WAQIfilename(x,y,z)):
        ##keep same format as fresh tile
        return 200, Image.open(WAQIfilename(x, y, z))

    return 400, Image.new('RGBA',(256,256),(0,0,0,0))

def cacheHandler(x,y,z):
    l = fileLastModified(cacheFilename(x,y,z),x,y,z)
    if l == -1 or overaday(l):
        return blur(x,y,z)

    ##sanity - already covered in above, but double check there is actually a file there
    if os.path.isfile(cacheFilename(x,y,z)):
        return Image.open(cacheFilename(x,y,z))

    return Image.new('RGBA',(256,256),(0,0,0,0))

def blur(x,y,z):
    imgTuple = WAQIcacheHandler(x, y, z)
    if imgTuple[0] == 200:
        ##image has content
        ##get surrounding to improve blur
        img = checkTileEdges(imgTuple[1],x,y,z)
        img = img.filter(ImageFilter.GaussianBlur())
        img = img.filter(ImageFilter.GaussianBlur(radius=8))
        img = img.crop((256,256,512,512))
        img.save(cacheFilename(x,y,z),'png')
        return img
    ##blank image
    return imgTuple[1]

##image paste helper
def ImageMerge(i1, i2, coords=(0,0)):
    if not i1.mode == "RGBA" or not i2.mode == "RGBA":
        i1 = i1.convert("RGBA")
        i2 = i2.convert("RGBA")

    r, g, b, a = i1.split()
    t = Image.merge("RGB", (r, g, b))
    m = Image.merge("L", (a,))
    i2.paste(t, coords, m)
    return i2


##improve blurring by getting bleed - could be simplified
##taking up to 6 seconds
@time_usage
def checkTileEdges(img, x, y, z):
    o = Image.new('RGBA', (768, 768), (0,0,0,0))

    extent = pow(2, z)-1
    if y > 0:
        if x > 0:
            upleft = WAQIcacheHandler(x - 1, y - 1, z)[1]
        else:
            upleft = WAQIcacheHandler(extent, y - 1, z)[1]

        if x < extent:
            upright = WAQIcacheHandler(x + 1, y - 1, z)[1]
        else:
            print(x,y,z)
            upright = WAQIcacheHandler(0, y - 1, z)[1]

        up = WAQIcacheHandler(x, y - 1, z)[1]
    else:
        if x > 0:
            upleft = WAQIcacheHandler(x - 1, extent, z)[1]
        else:

            upleft = WAQIcacheHandler(extent, extent, z)[1]

        if x < extent:
            upright = WAQIcacheHandler(x + 1, extent, z)[1]
        else:
            upright = WAQIcacheHandler(0, extent, z)[1]

        up = WAQIcacheHandler(x, extent, z)[1]

    o = ImageMerge(upright,o,(512,0,768,256))
    o = ImageMerge(upleft, o, (0, 0, 256, 256))
    o = ImageMerge(up, o, (256, 0, 512, 256))

    ##tiles surrounding in all 8 directions, then paste main portion on top
    if y < extent:
        if x > 0:
            downleft = WAQIcacheHandler(x - 1, y + 1, z)[1]
        else:
            downleft = WAQIcacheHandler(extent, y + 1, z)[1]

        if x < extent:
            downright = WAQIcacheHandler(x + 1, y + 1, z)[1]
        else:
            downright = WAQIcacheHandler(0, y + 1, z)[1]

        down = WAQIcacheHandler(x, y + 1, z)[1]
    else:
        if x > 0:
            downleft = WAQIcacheHandler(x - 1, 0, z)[1]
        else:
            downleft = WAQIcacheHandler(extent, 0, z)[1]

        if x < extent:
            downright = WAQIcacheHandler(x + 1, 0, z)[1]
        else:
            downright = WAQIcacheHandler(0, 0, z)[1]

        down = WAQIcacheHandler(x, 0, z)[1]


    o = ImageMerge(downright, o, (512, 512, 768, 768))
    o = ImageMerge(downleft, o, (0, 512, 256, 768))
    o = ImageMerge(down, o, (256, 512, 512, 768))

    if x > 0:
        left = WAQIcacheHandler(x - 1, y, z)[1]
    else:
        left = WAQIcacheHandler(extent, y, z)[1]

    o = ImageMerge(left,o, (0, 256, 256, 512))

    if x < extent:
        right = WAQIcacheHandler(x + 1, y, z)[1]
    else:
        print(x,y,z)
        right = WAQIcacheHandler(0, y, z)[1]

    o = ImageMerge(right, o, (512, 256, 768, 512))

    ##paste original tile in center
    o = ImageMerge(img, o, (256, 256, 512, 512))

    return o

##callback helper
def ImgCallBackBytes(img):
    img = img.resize((256, 256))
    imgBytes = io.BytesIO()
    img.save(imgBytes, format='PNG')
    imgBytes = imgBytes.getvalue()
    # return str(imgBytes)
    return imgBytes



##set up endpoints
app = Klein()

@app.route("/aqi/<int:x>/<int:y>/<int:z>", branch=True)
def aqiHandler(request,x,y,z):
    global a
    if not os.path.isdir(cacheDir(z)):
        os.mkdir(cacheDir(z))
    request.setHeader('content-type', 'image/png')
    a = threads.deferToThread(cacheHandler,x,y,z)
    return a.addCallback(ImgCallBackBytes)

@app.route("/")
def info(request):
    request.setHeader('content-type','text/plain')
    return "Air quality data provided by the World Air Quality Index project and the EPA.\nSee http://aqicn.org/ and http://aqicn.org/sources/ for more information."

##set up https if needed
https = False
for v in sys.argv:
    if v.lower() == 'https':
        https = True

endpointdesc = 'ssl:8088:privateKey='+privateKeyPath+':certKey='+certificatePath

if not https:
    endpointdesc = ''

##double check cache dir is there
if not os.path.isdir(cachePath):
    os.mkdir(cachePath)

#run the service
print("Running on 0.0.0.0")
app.run('0.0.0.0', 8088, endpoint_description=endpointdesc )
