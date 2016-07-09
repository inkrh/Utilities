##kaossilator pro plus CC to midi note
##a work in progress
import mido

mt = ''
nvalue = 0
##vvalue = 0
pnvalue = nvalue

def Translate(message,o):
    global mt
    global nvalue
    global vvalue
    
    if message.control == 92 and not message.value == 127:
        mt = 'note_off'
        o.send(mido.Message('note_off',note=nvalue))
    
    if message.control == 92 and message.value ==127:
        mt = 'note_on'

    
    ##microGranny - note range == ~48 to ~84
    if message.control == 12:
        n = message.value
        nNote = n%12
        cNote = n%36
        rNote = 48
        nvalue = rNote + nNote + cNote

##    if message.control == 13:
##        vvalue = max(100,message.value)


def ManualPanic(o):
    for i in range(0,128):
        o.send(mido.Message('note_off',note=i))

    
def Run():
    global mt
    global nvalue
    global pnvalue
    
    with mido.open_output(autoreset = True) as o:
        with mido.open_input() as i:
            while True:
                for message in i:
                    if message.type == 'control_change':## and not message.control == 13:
                        print("in : " + str(message))
                        Translate(message,o)
                        
                    if 'note' in mt:
                        if not pnvalue == nvalue:
                            mo = mido.Message(mt,note = nvalue, velocity = 100)
                            print("out : " + str(mo))
                            o.send(mo)
                            pnvalue = nvalue
                        ##microgranny tends not to respond to off or time, or anything it doesn't like
                        if 'off'in mt:
                            mt = ''
                            o.send(mido.Message('note_off',note = pnvalue))
                            o.send(mido.Message('note_off',note=nvalue))
                            print("out : note_off")
                            o.reset()
                            o.panic()
                            ManualPanic(o)

if __name__== '__main__':
    Run()
