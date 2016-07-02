import mido
import time

def Run(fi, minnote=21, maxnote=108, forcelowest=False, minvelocity=64, maxvelocity=115, timingdivisor=127, shortestnoteon=0.00390625, step=3, mono=True, microgranny=True, sendCC=True, sendsamplechange=True, loop=False):

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
                Play(o, b,minnote,maxnote, forcelowest, minvelocity, maxvelocity, timingdivisor,shortestnoteon,step,mono,microgranny,sendCC,sendsamplechange)
                
        else:
            Play(o, b,minnote,maxnote,forcelowest, minvelocity, maxvelocity,timingdivisor,shortestnoteon,step,mono,microgranny,sendCC,sendsamplechange)


def Play(o, b,minnote,maxnote,forcelowest, minvelocity, maxvelocity, timingdivisor,shortestnoteon,step,mono,microgranny,sendCC,sendsamplechange):
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

            ##because
            if microgranny:
                if sendsamplechange:
                    ##send sample change
                    if sn in range(0,6):
                        o.send(mido.Message('note_on', note = sn+1))
                        print("Sample change to "+ str(sn+1))

                    if sendCC:
                        ##send command change (sampleRate,crush,attack,release,grainSize,shiftSpeed,start,end)
                        if sn in range(105,111):
                            ##because I was annoyed by something
                            ##if sn != 104:
                            o.send(mido.Message('control_change',control=sn,value=sv))
                            print("Control change to " + str(sn) + " : " +str(sv))

            

            ##set min and max note (wrapping aroung maxnote)
            ##NB most randomly chosen files will have a lot of notes less than
            ##any given minnote
                                
            if forcelowest:
                sn = sn%maxnote
            else:
                noterange = maxnote-minnote
                sn = (sn%noterange)+minnote

                    
            ##set min and max velocity
            velocityrange = maxvelocity-minvelocity
            sv = (sv%velocityrange)+minvelocity
                

            ##because information
            print("Byte set " + str(i) + " : sn " + str(sn) + " : sv " + str(sv) + " : t " + str(t))


            ##send output, send as note off if below lowest (forcelowest)
            if sn < minnote:
                o.send(mido.Message('note_off', note=sn, time=t))
            else:
                o.send(mido.Message('note_on', note=sn, velocity=sv, time=t))

            ##one note at a time, sleep between messages
            if mono:
                time.sleep(t)
                ##cover not responding to time in mido.Message
                o.send(mido.Message('note_off', note=sn))

##examples of settings, let the randomness begin
##depends on file input but with image file of ~93kb step of 384 and divisor of 63.75 will be ~8.5 minutes
                
##good settings for microbrute
def MicroBrute(fi):
    Run(fi,minnote=48,maxnote=83,step=512, microgranny=False)

def MicroBruteLoop(fi):
    Run(fi,minnote=24,maxnote=47,step=192, microgranny=False, loop=True)

##microgranny
def MicroGrannyNoSampleChange(fi):
    Run(fi,minnote=48,maxnote=83,step=192, sendsamplechange=False)

def MicroGrannySampleChange(fi):
    Run(fi,minnote=48,maxnote=83, shortestnoteon=0.375, sendsamplechange=True, minvelocity=100)

