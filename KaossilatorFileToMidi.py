import mido
import time

def Run(fi, minnote=21, maxnote=108, minypad=0, maxypad=127, timingdivisor=127, shortestnoteon=0.00390625, step=3, loop=False):

    if minnote < 0:
        print("Negative minimum note")
        minnote = 0
        
    if maxnote >127:
        print("Maximum note too high")
        maxnote = 127

    if maxnote < minnote or minnote > maxnote:
        print("Maxnote and minnote swapped")
        hold = maxnote
        maxnote = minnote
        minnote = hold

    ##open file as a byte array
    with open(fi, "rb") as inFile:
        f = inFile.read()
        b = bytearray(f)

    ##send midi
    with mido.open_output() as o:
        if(loop):
            while True:
                Play(o, b,minnote,maxnote, minypad, maxypad, timingdivisor,shortestnoteon,step)
                
        else:
            Play(o, b,minnote,maxnote, minypad, maxypad, timingdivisor,shortestnoteon,step)


def Play(o, b,minnote,maxnote, minypad, maxypad, timingdivisor,shortestnoteon,step):
    for i in range(0,len(b)-2, step):
    ##because I wanted to just grab a small subset for a loop
    ##for i in range(23037,23046):
        
            ##note i, ypad i+1, time i+2
            sx = (b[i]+minnote)%127
            sy = (b[i+1]+minypad)%127
            
            ##is a better way of handling the timing but will fix it when I need to
            ##or when I feel like it, whichever happens first
            
            ##divisor of 63.75 == max 4 second, 127 = max of 2 second
            if timingdivisor == 0:
                t = max(shortestnoteon,b[i+2])
            else:
                t = max(shortestnoteon,b[i+2]/timingdivisor)


##            ##set min and max ypad
            ypadrange = maxypad-minypad
            sy = (sy%ypadrange)+minypad
            noterange = maxnote-minnote
            sx = (sx%noterange)+minnote
            ##pad pressed
            o.send(mido.Message("control_change",channel=0,control=92,value=127))
            ##x/y position of press
            o.send(mido.Message("control_change",channel=0,control=12,value=sx,time=0))
            o.send(mido.Message("control_change",channel=0,control=13,value=sy,time=0))
            print("Byte set " + str(i) + " : sx " + str(sx) + " : sy " + str(sy) + " : t " + str(t))

            time.sleep(t)
            ##pad released
            o.send(mido.Message("control_change",channel=0,control=92,value=0))

##examples of settings, let the randomness begin
                
##good settings for Kaossilator Pro Plus drum loops
def ProcessFile(fi):
    Run(fi,minnote=48,maxnote=83,step=512)

def ProcessFileLoop(fi):
    Run(fi,minnote=48,maxnote=60,step=192,timingdivisor=33,loop=True)
##good settings for Kaossilator Pro Plus non-looped voices
def IndividualProcessFileLoop(fi):
    Run(fi,minnote=0,maxnote=127,step=3,loop=True)
