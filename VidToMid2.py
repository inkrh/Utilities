import mido
from threading import Timer
import time
import random
import numpy as np
import cv2
from PIL import Image



def play(o,c):
    c = c[time.localtime().tm_sec]
   
    n = (int(c[0][0]/2)%48)+36
    v = (int(c[1][1]/2)%27)+100
    t = float(c[2][0])/float(256)
    o.send(mido.Message('note_on',note=n, velocity = v, time = t))
    

def stop(o,n):
    o.send(mido.Message('note_off',note=n))

def stopAll(o):
    for i in range(0,128):
        stop(o,i)

def camera(cap):
    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    copy = cv2.resize(image,(61,61))
    cv2.imshow("input",copy)
    return copy


def Run():
    ##start camera and open midi out
    cap = cv2.VideoCapture(0)
    o = mido.open_output(autoreset=True)
    ##then play
    try:
        while True:
            c = camera(cap)
            on = Timer((1/16),play(o,c))
            off = Timer(1,stopAll(o))
    ##ctrl-c to quit, closes camera and midi
    finally:
        cap.release()
        cv2.destroyAllWindows()
        o.close()

