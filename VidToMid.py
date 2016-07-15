import mido
import time
import random
import numpy as np
import cv2
from PIL import Image


def play(o,cap):
    
    c = camera(cap)
    print c
    n = (int(c[0])%48)+48
    v = (int(c[1])%27)+100
    tseed = c[2]
    r = random.Random(tseed)
    t = r.random()
    
    o.send(mido.Message('note_on',note=n,velocity=v))
    time.sleep(t/(t/2))
    o.send(mido.Message('note_off',note=n))
    time.sleep(t/(t/2))


def camera(cap):
    global seq
    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("input",image) 
    avg = np.average(image, axis=0)
    return np.average(avg, axis=0)
    
def Run():
    cap = cv2.VideoCapture(0)
    o = mido.open_output(autoreset=True)
    try:
        while True:
            play(o,cap)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        o.close()
