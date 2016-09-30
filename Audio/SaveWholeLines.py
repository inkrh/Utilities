import os
import string

def Process(inputTxtFile,outputPath):
    i = open(inputTxtFile)
    index = 0
    for line in i:

        if len(line) >0:
            o = os.path.join(outputPath,str(index)+'.wav')
            print o
            os.system('say -o ' + o + ' --data-format=LEF32@22050 "' + line + '"')
            index +=1
    i.close()
