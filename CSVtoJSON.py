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

        

def ConvertCSV(fileIn, fileOut):
    i = open(fileIn,'r')
    o = open(fileOut, 'w')
    outputJson = "{"
    titleLine = i.readline()
    titleArray = titleLine.split(',')
    actualTitleArray = []
    for item in titleArray:
        if len(item.strip()) > 0:
                actualTitleArray.append(item)

    outputJson = outputJson + "\"" + actualTitleArray[0] + "\":["
    
    for line in i:
        each = line.split(',')
        if len(each[0]) > 0:
            outputJson = outputJson + "{\"" + each[0] + "\":[{"
            for item in range(1,min(len(each),len(actualTitleArray))-1):
                if len(each[item]) > 0:
                    outputJson = outputJson + "\""+actualTitleArray[item] + "\":" + str(stringFloatOrInt(each[item])) +","
            if outputJson[len(outputJson)-1] == ",":
                outputJson = outputJson[:-1]
            outputJson = outputJson + "}]},"
        
    if outputJson[len(outputJson)-1] == ",":
        outputJson = outputJson[:-1]
    outputJson = outputJson + "]}"
    o.write(outputJson)

    o.close()
    i.close()


