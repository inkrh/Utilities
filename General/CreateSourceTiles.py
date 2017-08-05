##Generate Tile Data
from PIL import Image
import requests
import math
import os, sys, io
from pyproj import Proj, transform
import unittest

##NB CAN BE SLOW BUT ONCE SOURCE DATASETS ARE CREATED INCREASES SPEED

##each key only allows 20,000 to 50,000 uses per 24 hour period
##(conflicting information from Bing emails).
##for each zoom level > 9 multiple keys will be needed for the full set of data

##TODO if error returned switch to alt map key(s)

##full file size will be pow(pow(2,z),2)px

mapKey = "<your key>"

DEG_TO_RAD = math.pi/180
RAD_TO_DEG = 180/math.pi
ALLF = 0xFFFFFFFF
someFailed = False

##Bing maps detail range
MinLatitude =  -85.05112878
MaxLatitude = 85.05112878
MinLongitude = -180
##elevations API throws an error if 180
MaxLongitude = 179.99999999
##using full8 as general rule of thumb
WorkingImage = Image.open("full8.tiff")

##sends request to Bing Maps
def sendRequest(bounds):
    try:
        ##bounds is s,w,n,e
        boundsString = str(bounds[0])+","+str(bounds[1])+","+str(bounds[2])+","+str(bounds[3])
        
        requestString = "http://dev.virtualearth.net/REST/v1/Elevation/Bounds?bounds="+boundsString+"&rows=32&cols=32&key="+mapKey

        result = requests.get(requestString)
        if result.status_code == 200:
            return result.json()['resourceSets'][0]['resources'][0]['elevations']
        print (result.content)
        return result.status_code
    except:
        print ("Request failed")
        return -1

def convertto2D(elevationsList):
    if type(elevationsList)==int:
        print("Error from elevations : " + str(elevationsList))
        return False
    result = []
    for i in range(0,1024,32):
        x = elevationsList[i:i+32]
        result.append(x)    
    return result

def mapSize(self,levelOfDetail):
    return (256 << levelOfDetail) & ALLF
           
def LatLongBoundsFromXYZ(x,y,z):
    e = tile2lon(x+1,z)
    w = tile2lon(x,z)
    s = tile2lat(y+1,z)
    n = tile2lat(y,z)
    
##get conversion factor
    sfactor,wfactor = Convert(s,w)
    nfactor,efactor = Convert(n,e)
## apply conversion factor
    s = Clip(s - sfactor,MinLatitude,MaxLatitude)
    w = Clip(w - wfactor,MinLongitude,MaxLongitude)
    e = Clip(e + efactor,MinLongitude,MaxLongitude)
    n = Clip(n + nfactor,MinLatitude,MaxLatitude)
    
    return [s,w,n,e]

def Clip(n,minValue,maxValue):
    return min(max(n,minValue),maxValue)

def tile2lat(y,z):
    n = math.pi -2 * math.pi * y / math.pow(2,z)
    return RAD_TO_DEG * math.atan(0.5 * (math.exp(n) - math.exp(-n)))
    
def tile2lon(x,z):
    return x / math.pow(2,z) * 360 - 180
          
##create a black image, with elevations set to 0+elevation up to 255
def processImage(elevationsList):
    if type(elevationsList) == bool:
        return False
##unneeded if using previously fetched data
##    counter = 0
##    ##only save images with detail - assume images not present are sea
##    for x in range(32):
##        for y in range(32):
##            counter = counter + elevationsList[x][y]
##    print counter
##    if counter <= 0:
##    if all(all(j <=0 for j in i) for i in elevationsList):
##        return 2
##    if all(j >=255 for j in elevationsList):
##        return Image.new('L',(32,32),(255))
    
    img = Image.new('L',(32,32),(0))
    pixels = img.load()
    for x in range(32):
        for y in range(32):
            if elevationsList[x][y] > 0:
                e = min(elevationsList[x][y],255)
                pixels[x,y] = (e)
 
    return img


##check against a grayscale tile for that level
def checkImage(source, level):
    i = Image.open(source)
    pixelsIn = i.load()
    o = Image.new('RGBA',(32,32),(152,177,224,128))
    pixelsOut = o.load()
    
    for x in range(32):
        for y in range(32):
            if pixelsIn[x,y] >= level:
                pixelsOut[x,y] = (229,min(240+pixelsIn[x,y][0],255),220,128)
            else:
                pixelsOut[x,y] = (152,152,min(177+pixelsIn[x,y][0],255),128)
                
    return o

##returns true if WorkingImage has content for that area
##cut down # of calls
def doIGetTile(x,y):
    return True
    xs = 32*x
    ys = 32*y
    ##crop is taking up a lot of time
    im = WorkingImage.crop((xs,ys,xs+32,ys+32))

## Validity test, pull out cropped tile and check independently
##    return im
    
## old method
##    p = im.load()
##    for i in range(32):
##        for j in range(0,32):
##           # print(str(p[i,j]))
##            if p[i,j] >0:
##                print("Found a pixel >0 at "+str(i)+":"+str(j))
##                return True
##    return False
    
##new method
    if all(pi<=0 for pi in im.getdata()):
        return False

    return True

##checks tiles surrounding x,y
##returns true if any are !sea
##we were losing some detail
def CheckSurrounding(x,y,z):
    ##edges - just say yes
    if x<=0 or y <=0 or x>=pow(2,z) or y>=pow(2,z):
        return True
    ##+1-1
    getOrNot = False
    for i in range(-1,2):
        for j in range(-1,2):
            if doIGetTile(x,y):
                getOrNot = True

    return getOrNot
    
##main tile creation script
def render_tile(name,x,y,z,log, force = False, level = 0):
    
    bounds = LatLongBoundsFromXYZ(x,y,z)
#    print bounds

    if force:
        f = processImage(convertto2D(sendRequest(bounds)))
    else:
        if (doIGetTile(x,y) or CheckSurrounding(x,y,z)):
            f = processImage(convertto2D(sendRequest(bounds)))
        else:
            f = 2

        
#    f = checkImage("sourcetiles_"+str(z),level)
    
    log.write('img ' + str(x) + ',' + str(y) + ','+str(z)+','+str(level)+"\n")
 #   print(str(x)+" " + str(y) + " " + str(z))
    if type(f)==bool:
        log.write("Request Failed - " + str(x)+" " + str(y) + " " + str(z) + "\n")
        print("Request Failed - " + str(x)+" " + str(y) + " " + str(z) + "\n")
        someFailed = True

        return -1
    elif type(f)==int:
#        print("Skipping Tile")
        log.write("Skipping "+str(x)+" " + str(y) + " " + str(z)+" - it is sea\n")
        return 0
    else:
#        print("Saving Tile - " + name)
        log.write("Saving this tile - " + name + "\n")
        f.save(name, "TIFF")
        return 0
    
##return byte array from image
def bytes(filename):
    with open(filename, "rb") as imageFile:
                f = imageFile.read()
                bytes = bytearray(f)
                return bytes

def Test(path, zoomlevel,log):
    log.write("Path " + path + "; zoom " + str(zoomlevel))
    extent = pow(2,zoomlevel)-1
    for x in range(extent+1):
        for y in range(extent+1):
            filename = path+"/tile_" + str(x) + "_" + str(y) + "_" + str(zoomlevel) + ".tiff"
            if render_tile(filename,x,y,zoomlevel,log) == -1:
                log.write("Failed on "+str(x) + ":" + str(y) + " :z " + str(z))
                log.write("Try a new map key")
                return False
    return True

##partial set of tiles for an area
def FixAPIRejected(xmin,xmax,ymin,ymax,zoomlevel, force = False):
    global WorkingImage
    log = open("fixlog.txt",'w')
    log.write("Fixing " +str(xmin) + " to " + str(xmax) + " : " + str(ymin) + " to " + str(ymax) + "\n")
    print("Fixing " +str(xmin) + " to " + str(xmax) + " : " + str(ymin) + " to " + str(ymax) + "\n")

    path = "sourcetiles_"+str(zoomlevel)
    s = 32 * pow(2,zoomlevel)
    ##resize is taking up a lot of time
    WorkingImage = WorkingImage.resize((s,s))
    for x in range(xmin,xmax+1):
        print("Working on X: "+str(x))
        for y in range(ymin,ymax+1):
            filename = path+"/tile_" + str(x) + "_" + str(y) + "_" + str(zoomlevel) + ".tiff"
            render_tile(filename,x,y,zoomlevel,log, force)
    log.close()


##create one full image (will cause bomb error on z>9)    
def Collate(path, zoomlevel):
    extent = pow(2,zoomlevel)    
    outImage = Image.new('L',(32*extent,32*extent),(0))
    for x in range(extent+1):
        for y in range(extent+1):
            filename = path+"/tile_" + str(x) + "_" + str(y) + "_" + str(zoomlevel) + ".tiff"
            if(os.path.isfile(filename)):
               o = Image.open(filename)
               o = o.rotate(90,expand=True)
               outImage.paste(o,(32*(x-xr[0]),32*(y-yr[0])))


    outImage.save(path+"/full"+str(zoomlevel)+".tiff","TIFF")
    outImage.show()

##create a full set of quarter images
def MultipleFull(path,zoomlevel):
    extent = pow(2,zoomlevel)
    each = extent/2
    a = [0,each]
    b = [each+1,extent]
    CreateFull(path+"/10_AA_AB",zoomlevel,a,a,'aa',(32*each,32*each))
    CreateFull(path+"/10_AA_AB",zoomlevel,a,b,'ab',(32*each,32*each))
    CreateFull(path+"/10_BA_BB",zoomlevel,b,a,'ba',(32*each,32*each))
    CreateFull(path+"/10_BA_BB",zoomlevel,b,b,'bb',(32*each,32*each))

##create a quarter image
def CreateFull(path,zoomlevel,xr,yr,name,s):
    print(xr,yr)
    outImage = Image.new('L',s,(0))
    for x in range(xr[0],xr[1]+1):
        for y in range(yr[0],yr[1]+1):
            filename = path+"/tile_" + str(x) + "_" + str(y) + "_" + str(zoomlevel) + ".tiff"
            if(os.path.isfile(filename)):
                print("Found fileName : " + filename)
                o = Image.open(filename)
                o = o.rotate(90,expand=True)
                outImage.paste(o,(32*(x-xr[0]),32*(y-yr[0])))

    outImage.save(path+"/full"+str(zoomlevel)+name+".tiff","TIFF")
    outImage.show()
    
##main body - runs tile creation service
def RunSvc(zoomlevelStart,zoomlevelEnd):
    someFailed = False
    log = open("log.txt",'w');
    for zoomlevel in range(zoomlevelStart,zoomlevelEnd+1):
        fn = "sourcetiles_"+str(zoomlevel)
        os.system('mkdir '+fn)
        if Test(fn,zoomlevel,log) == False:
            log.close()
            break
        try:
            Collate(fn,zoomlevel)
        except:
            log.write("Failure on "+str(zoomlevel))
    log.close()
    FindFailed("log.txt")

##total space if fetching _all_ tiles for a zoom range
def SpaceNeeded(startzoom,stopzoom):
    total = 0
    for i in range(startzoom,stopzoom):
        total = (total+(1024*(((2**i)-1)**2)))
    
    return total

##not really used but nice to have
def TileMax(zoom):
    return pow(2,zoom)-1

##works ferpectly for iOS maps, may need adjustment for Bing maps.
def Convert(x1,y1):
    
    inProj = Proj(init='epsg:3857')
    outProj = Proj(init='epsg:4326')

    x2,y2 = transform(inProj,outProj,x1,y1)
    
    return x2,y2

def FindFailed(fi):
    someFailed = False
    ##avoid overwriting fixlog if failures repeat
    os.system("cp "+fi+" "+fi+".BKUP.txt")
    
    i = open(fi)
    for lines in i.readlines():
        if "Failed" in lines:
            retryString = lines.replace("Request Failed - ","")
            retry = retryString.split(" ")
            FixAPIRejected(int(retry[0]),int(retry[0]),int(retry[1]),int(retry[1]),int(retry[2]),force = True)
    i.close()
    if someFailed:
        print("Requests still failed. Check map key and connection.")
        print("Original file saved as " + fi+".BKUP.txt")


##Check connection and source is there on exec
class LaunchTest(unittest.TestCase):
    def test_Connection(self):
        self.assertFalse(sendRequest(LatLongBoundsFromXYZ(0,0,1))==-1)

    def test_Source(self):
        self.assertFalse(WorkingImage == None)

t = unittest.TestLoader().loadTestsFromTestCase(LaunchTest)
unittest.TextTestRunner(verbosity=3).run(t)


##if __name__ == '__main__':
##    try:
##        RunSvc(sys.argv[1],sys.argv[2])
##    except:
##        print("failed - check logs")
