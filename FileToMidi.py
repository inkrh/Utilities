import mido
import time

def Run(fi, minnote=21, maxnote=108, minvelocity=64, timingdivisor=127, shortestnoteon=0.00390625, step=3, mono=True, microgranny=True, sendCC=True, sendsamplechange=True, loop=False):

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
        
    if timingdivisor == 0:
        print "Timing divisor can't be 0"
        return

    ##open file as a byte array
    with open(fi, "rb") as inFile:
        f = inFile.read()
        b = bytearray(f)

    ##send midi
    with mido.open_output() as o:
        if(loop):
            while True:
                Play(o, b,minnote,maxnote,minvelocity,timingdivisor,shortestnoteon,step,mono,microgranny,sendCC,sendsamplechange)
                
        else:
            Play(o, b,minnote,maxnote,minvelocity,timingdivisor,shortestnoteon,step,mono,microgranny,sendCC,sendsamplechange)


def Play(o, b,minnote,maxnote,minvelocity,timingdivisor,shortestnoteon,step,mono,microgranny,sendCC,sendsamplechange):
    for i in range(0,len(b)-2, step):
   ## for i in range(23037,23046):
            ##note i, velocity i+1, time i+2
            sn = b[i]%127
            sv = b[i+1]%127
            
            ##is a better way of handling the timing but will fix it when I need to
            ##divisor of 63.75 == max 4 second, 127 = max of 2 second
            t = max(shortestnoteon,b[i+2]/timingdivisor)

            if microgranny:
                if sendsamplechange:
                    ##send sample change
                    if sn in range(0,6):
                        o.send(mido.Message('note_on', note = sn))
                        print("Sample change to "+ str(sn))

                    if sendCC:
                        ##send command change (sampleRate,crush,attack,release,grainSize,shiftSpeed,start,end)
                        if sn in range(102,111):
                            o.send(mido.Message('control_change',control=sn,value=sv))
                            print("Control change to " + str(sn) + " : " +str(sv))

            ##set min velocity
            sv = max(sv,minvelocity)

            ##set min and max note (wrapping aroung maxnote)
            sn = sn%maxnote
            sn= max(minnote,sn)
 
            ##because
            print("Byte set " + str(i) + " : sn " + str(sn) + " : sv " + str(sv) + " : t " + str(t))

            ##send output
##            if sn < minnote:
##                o.send(mido.Message('note_off', time = t))
##            else:
            o.send(mido.Message('note_on', note=sn, velocity=sv, time=t))

            ##one note at a time
            if mono:
                time.sleep(t)
                ##cover not responding to time in above
                o.send(mido.Message('note_off', note=sn))

##good settings
##depends on file input but with image file of ~93kb step of 384 and divisor of 63.75 will be ~8.5 minutes
                
##good settings for microbrute
def MicroBrute(fi):
    Run(fi,minnote=24,maxnote=47,step=192, microgranny=False)

def MicroBruteLoop(fi):
    Run(fi,minnote=24,maxnote=47,step=192, microgranny=False, loop=True)


def MicroGrannyNoSampleChange(fi):
    Run(fi,minnote=48,maxnote=83,step=192,microgranny=True, sendsamplechange=False, loop=True)

def MicroGrannySampleChange(fi):
    Run(fi,minnote=48,maxnote=83,step=192)


