def isInt(s):
    try:
        int(s)
        return int(s)
    except:
        return False

def isFloat(s):
    try:
        float(s)
        return float(s)
    except:
        return False

def stringFloatOrInt(s):
    if s == "0":
        return 0
    
    if isInt(s):
        return isInt(s)
    
    if isFloat(s):
        return isFloat(s)

    return "\""+str(s)+"\""

        

def ConvertKaraokeFile(fileIn, fileOut):
    i = open(fileIn,'r')
    o = open(fileOut, 'w')
    track = "Track"
    artist = "Artist"
    
    output = "["

    for line in i:
        m = line.replace(chr(13),'')
        m = m.replace(chr(10),'')
##        for i in m:
##            print(str(i) + " : " + str(ord(i)))
        
        t = m.split(',')
        if len(t)==2:
            output = output +"{\""+track+"\":\""+t[0]+"\",\""+artist+"\":\""+t[1]+"\"},"
    
    if output.endswith(","):
        output = output[:-1]
    output = output +"]"
    
    o.write(output)
    o.close()
    i.close()


