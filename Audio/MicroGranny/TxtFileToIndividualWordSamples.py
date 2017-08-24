import os
import string

def Process(inputTxtFile,outputPath):
    i = open(inputTxtFile)
    for line in i:
        words = line.split(' ')
        if len(words) > 0:
            for word in words:
                fo = Filter(word.replace('\n','')).lower()+'.wav'
                
                if len(fo) > 4:
                    o = os.path.join(outputPath,fo)
                    print o
                    os.system('say -o ' + o + ' --data-format=LEF32@22050 "' + word + '"')
    i.close()
    
        
        
def Filter(word):
    o = ""
    for letter in word:
        if letter in string.ascii_letters or letter in string.digits:
            o = o + letter

    return o

