from pydub import AudioSegment
import os

def splitSong(fi,chunks):
    ##could use extension from Process() but this makes it more reusable
    print "Processing " + fi
    extension = fi[fi.index('.')+1:]
    song = AudioSegment.from_file(fi,extension)
    oldName = fi[:fi.index('.')]
    c = 0
    size = len(song)/chunks
    for i in range(0,len(song),size):
        o = song[i:i+size]
        newName = oldName+"_"+str(c)+"."+extension        
        print "\tas " +str(i)+ " to " + str(i+size)
        print "\tsaving as " + newName
##forcing wav here since I am having issues with my python ffmpeg svc
##        o.export(newName,format='wav')
##otherwise is
        o.export(newName,format=extension)
        c += 1


def listFilesWithExt(path, extension):
    return [os.path.join(path,f) for f in os.listdir(path) if f.lower().endswith('.'+extension.lower())]

def Process(path,chunks,extension):
    for i in listFilesWithExt(path,extension):
        splitSong(i,chunks)
