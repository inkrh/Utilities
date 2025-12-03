from pydub import AudioSegment
import random

def Process(source,codec =""):
    if len(codec)<=0 and len(source)>3:
        codec = source[-3:]

    song = AudioSegment.from_file(source,codec)

    songarray = []

    step = len(song)/100
    for i in range(0,len(song),step):
        songarray = songarray + [song[i:i+step]]

    out = songarray[0]
    
    for i in range(1,len(songarray)):
        if random.randint(1,5)<3:
            if random.randint(1,20)<8:
                if i<len(songarray)-2 and i>1:
                    out = out + songarray[i+random.randint(0,2)]
            if random.randint(2,42)<16:
                out = out + songarray[i].reverse()
                
            out = out + songarray[i]

            if random.randint(3,42)<32:
                out = out + songarray[i]
        else:
            out = out + songarray[i]

    out.export("glitched.wav", format="wav")
    
