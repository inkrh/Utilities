import mido
import time

def Run(fi, minnote=21,maxnote=108, minvelocity=21, timingdivisor=127, shortestnoteon=0.00390625, step=3, mono=True):

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
        sn = b[i]
        sv = b[i+1]
        t = max(shortestnoteon,b[i+2]/timingdivisor)

        ##there is a far better way to do this, but I need sleep
        
        ##wraparound 0<sn<255 to 0<sn<127 should make this wraparound at min/max notes
        if sn > 127:
            sn = sn/2
            
        if sv > 127:
            sv =sv/2

        
        sv = max(sv,minvelocity)
        
        sn= max(minnote,min(maxnote,sn))
        
        print("Byte set " + str(i) + " : sn " + str(sn) + " : sv " + str(sv) + " : t " + str(t))

        o.send(mido.Message('note_on', note=sn, velocity=sv, time=t))

        if mono:
            time.sleep(t)

