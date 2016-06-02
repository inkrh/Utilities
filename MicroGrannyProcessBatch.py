from pydub import AudioSegment
import os

def splitSong(fi,prefix, chunkSize):
    print "processing " + fi
    if fi.endswith(".mp3"):
        song = AudioSegment.from_mp3(fi)
    else:
        extension = fi[fi.index('.')+1:]
        song = AudioSegment.from_file(fi,extension)
    count = 0
    suffix = ''
    if(len(song) > chunkSize):
        for i in range(chunkSize,len(song),chunkSize):
            o = song[:i]
            if count < 10:
                suffix = str(count)
            elif count > 9 and count < 16:
                suffix = hex(count).replace('0x','').capitalize()
            else:
                break
            oreduced = o.set_channels(1)
            oreduced = o.set_sample_width(2)
            oreduced = o.set_frame_rate(22050)
            print prefix+str(suffix)+".wav"
            oreduced.export(prefix+str(suffix)+".wav",format='wav')
            count = count + 1
                
            
    else:
        song.export(prefix+str(0)+".wav", format='wav')


def listFilesWithExt(path, extension):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.'+extension)]


def Process(path,outputPath,extension):
    startChar = 65
    maxUpper = 90
    startLower = 97
    maxLower = 122
    current = 65
    for i in listFilesWithExt(path,extension):
        prefix = chr(current)
        splitSong(i,outputPath+"/"+prefix,10000)
        current = current +1
        if current > maxUpper and current < startLower:
            current = startLower
        if current > maxLower:
            return "maxLower reached"

    return "done"
        
