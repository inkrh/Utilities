import os
##from subprocess import call

def listFilesWithExt(path, extension):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.'+extension)]


def Process(path,extensionIn,extensionOut,fileOut):
    f = open(fileOut,'w')
    for root,subdirs,files in os.walk(path):
        for fi in files:
           if fi.endswith(extensionIn):
                fp = os.path.join(root,fi)
                
                fo = fp[:-len(extensionIn)]+extensionOut
                c = 'ffmpeg -i "'+fp+'" "'+fo+'"\n'
                print c
                f.write(c)
    f.close()
        
        

