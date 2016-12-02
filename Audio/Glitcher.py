from pydub import AudioSegment
import random

def Process(source,codec =""):
    if len(codec)<=0 and len(source)>3:
        codec = source[-3:]

    song = AudioSegment.from_file(source,codec)

    songarray = []

    step = len(song)/1000
    for i in range(0,len(song),step):
        songarray = songarray + [song[i:i+step]]

    out = songarray[0]
    
    for i in range(1,len(songarray)):
        if random.randint(1,20)<12:
            out = out + songarray[random.randint(0,len(songarray)-1)]
        if random.randint(2,42)<30:
            out = out + songarray[i].reverse()
            
        out = out + songarray[i]

        if random.randint(3,42)<40:
            out = out + songarray[i]


    out.export("glitched.wav", format="wav")
    
