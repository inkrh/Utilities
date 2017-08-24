from pydub import AudioSegment
import os
import string

fn1 = string.ascii_uppercase
fn2 = string.digits+string.ascii_uppercase

def convertTrack(fi,fo):
    outData = ""
    print "processing " + fi

    outData = outData + fi + " >> "
    
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
    return [os.path.join(path,f) for f in os.listdir(path) if f.lower().endswith('.'+extension.lower())]

def OutFileName(i):
    return fn1[i/len(fn2)]+fn2[i%len(fn2)]+".wav"

def Process(path,outputPath,extension):
    o = open(outputPath+"/index.txt",'w')
    fail = open(path+"/failed.txt",'w')
    index = 0
    items = listFilesWithExt(path,extension)
    items.sort()
    for fi in items:
        fo = OutFileName(index)
        try:
            o.write(convertTrack(fi,outputPath+"/"+fo))
        except:
            failText = "!!! " +fi+" failed try running ffmpeg on this file from the command line. !!!\n"
            print(failText)
            fail.write(failText)
            
        index += 1
        if index > (len(fn1)*len(fn2))-1:
            o.close()
            fail.close()
            return "maxUpper reached"

    fail.close()
    o.close()
    return "done"
        
