import mido
import time

def Run(fi, minnote=21, maxnote=108, minvelocity=100, maxvelocity=115, timingdivisor=127, shortestnoteon=0.00390625, step=3, loop=False):

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
                Play(o, b,minnote,maxnote, minvelocity, maxvelocity, timingdivisor,shortestnoteon,step)
                
        else:
            Play(o, b,minnote,maxnote, minvelocity, maxvelocity, timingdivisor,shortestnoteon,step)


def Play(o, b,minnote,maxnote, minvelocity, maxvelocity, timingdivisor,shortestnoteon,step):
    for i in range(0,len(b)-2, step):
    ##because I wanted to just grab a small subset for a loop
    ##for i in range(23037,23046):
        
            ##note i, velocity i+1, time i+2
            sn = (b[i]+minnote)%127
            sv = (b[i+1]+minvelocity)%127
            
            ##is a better way of handling the timing but will fix it when I need to
            ##or when I feel like it, whichever happens first
            
            ##divisor of 63.75 == max 4 second, 127 = max of 2 second
            if timingdivisor == 0:
                t = max(shortestnoteon,b[i+2])
            else:
                t = max(shortestnoteon,b[i+2]/timingdivisor)


##            ##set min and max velocity
            velocityrange = maxvelocity-minvelocity
            sv = (sv%velocityrange)+minvelocity

            o.send(mido.Message("control_change",channel=0,control=92,value=127))
            
            o.send(mido.Message("control_change",channel=0,control=12,value=sn,time=0))
            o.send(mido.Message("control_change",channel=0,control=13,value=sv,time=0))
            print("Byte set " + str(i) + " : sn " + str(sn) + " : sv " + str(sv) + " : t " + str(t))

            time.sleep(t)
            o.send(mido.Message("control_change",channel=0,control=92,value=0))

##
##            ##send output, send as note off if below lowest (forcelowest)
##            if sn < minnote:
##                o.send(mido.Message('note_off', note=sn, time=t))
##            else:
##                o.send(mido.Message('note_on', note=sn, velocity=sv, time=t))
##
##            ##one note at a time, sleep between messages
##            if mono:
##                time.sleep(t)
##                ##cover not responding to time in mido.Message
##                o.send(mido.Message('note_off', note=sn))

##examples of settings, let the randomness begin
##depends on file input but with image file of ~93kb step of 384 and divisor of 63.75 will be ~8.5 minutes
                
##good settings for Kaossilator Pro Plus drum loops
def ProcessFile(fi):
    Run(fi,minnote=48,maxnote=83,step=512)

def ProcessFileLoop(fi):
    Run(fi,minnote=48,maxnote=60,step=192,timingdivisor=33,loop=True)

def IndividualProcessFileLoop(fi):
    Run(fi,minnote=48,maxnote=60,step=192,timingdivisor=127,loop=True)
