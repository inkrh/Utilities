from pydub import AudioSegment
import sys

def changeSpeedandSave(file_path,speed=1.0):
    sound = AudioSegment.from_mp3(file_path)
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})
    output_file_path=file_path[:-4]+"_"+str(speed)+".mp3"
    sound_with_altered_frame_rate.export(output_file_path, format="mp3")
    

if __name__ == '__main__':
    if len(sys.argv)>1:
        print("Input mp3 file : "+ str(sys.argv[1]))
        print("Speed set to : "+ str(sys.argv[2]))
        try:
            changeSpeedandSave(sys.argv[1],float(sys.argv[2]))
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("Syntax python3 "+sys.argv[0]+" <file.mp3> <speed as float (e.g. 0.75)>")

