import csv

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
    r = csv.reader(i)
    a = []
    for row in r:
        a.append([row])
    print(len(a))
    print(len(a[0][0]))
    output = "[{"

    for rows in range(1,len(a)-1):
        for column in range(0,len(a[0][0])-1):
            output = output + "\"" + a[0][0][column] + "\":" + str(stringFloatOrInt(a[rows][0][column])) +","

        output = output[:-1]
        output = output + "},{"
        
    output = output[:-2]
    output= output+"}]"
    o.write(output)
    o.close()
    i.close()


