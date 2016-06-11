from pydub import AudioSegment
import os

def convertTrack(fi,fo):
    outData = ""
    print "processing " + fi
    outData = outData + fi + "\n"
    if fi.endswith(".mp3"):
        song = AudioSegment.from_mp3(fi)
    else:
        extension = fi[fi.index('.')+1:]
        song = AudioSegment.from_file(fi,extension)
        
    oreduced = song.set_channels(1)
    oreduced = oreduced.set_sample_width(2)
    oreduced = oreduced.set_frame_rate(22050)
        
    outData = outData + fo+"\n"
    print fo
    oreduced.export(fo,format='wav')
    return outData

def listFilesWithExt(path, extension):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.'+extension)]

def OutFileName(char1Asc,char2Asc):
    c1 = chr(char1Asc)
    if char2Asc < 10:
        c2 = str(char2Asc)
    else:
        c2 = hex(char2Asc).replace('0x','').capitalize()
        
    return c1+c2+".wav"

def Process(path,outputPath,extension):
    o = open(outputPath+"/index.txt",'w')
    startChar = 65
    maxUpper = 90
    current = 65
    secondCharLimit = 15
    current2 = 0
    for i in listFilesWithExt(path,extension):
        fo = OutFileName(current,current2)
        
        o.write(convertTrack(i,outputPath+"/"+fo))
        current2 = current2 + 1
        if current2 > secondCharLimit:
            current2 = 0
            current = current + 1
            if current > maxUpper:
                return "maxUpper reached"

            
    o.close()
    return
        
