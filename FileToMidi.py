import mido

def Run(fi):
    with open(fi, "rb") as imageFile:
        f = imageFile.read()
        b = bytearray(f)
    
    old = 0
    o = mido.open_output()
    for i in range(0,len(b)-1):
        sn = b[i]
        sv = b[i+1]
        if sn > 127:
            sn = sn/2
        if sv > 127:
            sv =sv/2

        o.send(mido.Message('note_on', note=sn, velocity=sv))
        o.send(mido.Message('note_off', note=old))

        old = sn

    o.send(mido.Message('note_off',note=old))

