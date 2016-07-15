import mido
import time
import random
import numpy as np
import cv2
from PIL import Image

w = 0.1

def play(o,r,cap):
    
    for i in range(0,len(camera(cap))):
        t = camera(cap)
        n = (t[i][0]%48)+48
        v = (t[i][1]%27)+100
                   
        o.send(mido.Message('note_on',note=n,velocity=v))
        time.sleep(r.random())
        o.send(mido.Message('note_off',note=n))
        time.sleep(r.random())


def camera(cap):
    global seq
    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('input',image)
    
    image.resize((3,3))
    return image

    
def Run():
    global w

    ##give some sort of swing
    r = random.Random(w)
    cap = cv2.VideoCapture(0)
    o = mido.open_output(autoreset=True)
    try:
        while True:
            play(o,r,cap)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        o.close()
