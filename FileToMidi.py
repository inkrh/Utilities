import mido
import time

def Run(fi, timingdivisor=127, shortestnoteon=0.3125):
    with open(fi, "rb") as imageFile:
        f = imageFile.read()
        b = bytearray(f)
    
    o = mido.open_output()
    for i in range(0,len(b)-2):
        sn = b[i]
        sv = b[i+1]
        t = b[i+2]
        
        if sn > 127:
            sn = sn/2
        if sv > 127:
            sv =sv/2
            
        print("sn " + str(sn) + " : sv " + str(sv) + " : t " + str(t))
        o.send(mido.Message('note_on', note=sn, velocity=sv, time=max(shortestnoteon,t/timingdivisor)))
        

