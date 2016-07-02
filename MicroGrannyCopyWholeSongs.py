from pydub import AudioSegment
import os
import string

fn1 = string.ascii_uppercase
fn2 = string.digits+string.ascii_uppercase

def convertTrack(fi,fo):
    outData = ""
    print "processing " + fi
    outData = outData + fi + " >> "
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

def OutFileName(i):
    return fn1[i/len(fn2)]+fn2[i%len(fn2)]+".wav"

def Process(path,outputPath,extension):
    o = open(outputPath+"/index.txt",'w')
    index = 0
    for fi in listFilesWithExt(path,extension):
        fo = OutFileName(index)
        
        o.write(convertTrack(fi,outputPath+"/"+fo))
        index += 1
        if index > (len(fn1)*len(fn2))-1:
            o.close()
            return "maxUpper reached"

            
    o.close()
    return
        
