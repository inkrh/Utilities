import mido
import time

def Run(fi, minnote=21, maxnote=108, minvelocity=64, timingdivisor=127, shortestnoteon=0.00390625, step=3, mono=True, microgranny=True):

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
    
    with open(fi, "rb") as imageFile:
        f = imageFile.read()
        b = bytearray(f)
    
    o = mido.open_output()
    for i in range(0,len(b)-2, step):
        sn = b[i]%127
        sv = b[i+1]%127
        t = max(shortestnoteon,b[i+2]/timingdivisor)

        if microgranny:

            ##send sample change
            if sn in range(0,6):
                o.send(mido.Message('note_on', note = sn))

            ##send command change (sampleRate,crush,attack,release,grainSize,shiftSpeed,start,end)
            if sn in range(102,111):
                o.send(mido.Message('control_change',control=sn,value=sv))


        sn = sn%maxnote
        
        sv = max(sv,minvelocity)
        
        sn= max(minnote,min(maxnote,sn))
        
        print("Byte set " + str(i) + " : sn " + str(sn) + " : sv " + str(sv) + " : t " + str(t))

        o.send(mido.Message('note_on', note=sn, velocity=sv, time=t))

        if mono:
            time.sleep(t)

