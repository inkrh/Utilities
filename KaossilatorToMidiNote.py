##kaossilator pro plus CC to midi note
##a work in progress
import mido

mt = ''
nvalue = 0
##vvalue = 0

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

    

    
def Run():
    global mt
    global nvalue
##    global vvalue
    
    with mido.open_output() as o:
        with mido.open_input() as i:
            while True:
                for message in i:
                    if message.type == 'control_change':
                        print("in : " + str(message))
                        Translate(message,o)
                        
                    if 'note' in mt:
                            mo = mido.Message(mt,note = nvalue, velocity = 100)
                            print("out : " + str(mo))
                            o.send(mo)
                            
