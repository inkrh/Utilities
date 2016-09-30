from pydub import AudioSegment
import os

def splitSong(fi,prefix, chunkSize):
    outData = ""
    print "processing " + fi
    outData = outData + fi + "\n"
    if fi.endswith(".mp3"):
        song = AudioSegment.from_mp3(fi)
    else:
        extension = fi[fi.index('.')+1:]
        song = AudioSegment.from_file(fi,extension)
    count = 0
    suffix = ''
    if(len(song) > chunkSize):
        for i in range(0,len(song),chunkSize):
            o = song[i:i+chunkSize]
            if count < 10:
                suffix = str(count)
            elif count > 9 and count < 16:
                suffix = hex(count).replace('0x','').capitalize()
            else:
                print "max samples in slot reached"
                break
            
            oreduced = o.set_channels(1)
            oreduced = oreduced.set_sample_width(2)
            oreduced = oreduced.set_frame_rate(22050)
            
            outData = outData + prefix+str(suffix)+".wav\n"
            print prefix+str(suffix)+".wav"
            oreduced.export(prefix+str(suffix)+".wav",format='wav')
            count = count + 1
                
            
    else:
        song.export(prefix+str(0)+".wav", format='wav')

    return outData

def listFilesWithExt(path, extension):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.'+extension)]


def Process(seconds, path,outputPath,extension):
    o = open(outputPath+"/index.txt",'w')
    
    chunkSize = seconds*1000
    startChar = 65
    maxUpper = 90
    current = 65
    for i in listFilesWithExt(path,extension):
        prefix = chr(current)
        o.write(splitSong(i,outputPath+"/"+prefix,chunkSize))
        current = current + 1
        if current > maxUpper:
            return "maxUpper reached"
    o.close()
    return
        
