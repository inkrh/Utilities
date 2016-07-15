

import mido
import time
import random
import numpy as np
import cv2
from PIL import Image


def play(o,cap):
    ##extra while loop is overkill, but means that the camera is definitely hit
    ##also makes sure that 0 length color data doesn't crash
    while len(camera(cap))>0:
        c=camera(cap)
        ##using R as note, limiting to MicroGranny's good range 48<=n<96
        ##should probably be 48 to 84...
        n = (int(c[0])%48)+48
        ##because
 ##       v = (int(c[1])%27)+100
        v=127
        ##using B as a seed for random timing
        tseed = c[2]
        r = random.Random(tseed)
        t = r.random()        
        o.send(mido.Message('note_on',note=n,velocity=v))
        #monophony, MG doesn't always like time messages
        ##dropping secs of note_on from 0.0<=t<1.0 to 0.0<=t<0.5
        time.sleep(t/(t/2))
        o.send(mido.Message('note_off',note=n))
        ##uncomment for gap after note_off
##        time.sleep(t/(t/2))


def camera(cap):
    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    ##show camera image
    cv2.imshow("input",image)
    ##average camera image data
    avg = np.average(image, axis=0)
    ##return average color
    return np.average(avg, axis=0)
    
def Run():
    ##start camera and open midi out
    cap = cv2.VideoCapture(0)
    o = mido.open_output(autoreset=True)
    ##then play
    try:
        while True:
            play(o,cap)
    ##ctrl-c to quit, closes camera and midi
    finally:
        cap.release()
        cv2.destroyAllWindows()
        o.close()

