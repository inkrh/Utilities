import sqlite3
from klein import Klein
import json

homeZIP = 10001
basePrices = {"Item1":100,"Item2":200,"Item3":300}
dbName = "ZipToPrice.db"
port = 9090

##e.g.
# basePrices = {"AutoLockout":100,"HomeLockout":200,"Jumpstart":300}




def ZipToPrice(zip):
    ##ensure type is right, try correcting
    if not type(zip)== int:
        try:
            zip = int(zip)
        except:
            return -99

    ##home area
    if zip == homeZIP:
        return 1

    try:
    ##do lookup of distance
        con = sqlite3.connect(dbName)
        cur = con.cursor()
        q = "select * from ZipMultiplier where ZIP == " +str(zip)
        cur.execute(q)
        results = cur.fetchall()
        con.close()
        ##no results
        if len(results)<=0:
            return -99
        #use first result from >=1 results
        return results[0][1]
    except:
        ##catchall
        return -99



def LookUpZip(zip):
    multiplier = ZipToPrice(zip)
    keyList = list(basePrices.keys())
    data = {}
    element = {}

    if not multiplier==-99:
        for i in range(len(basePrices.keys())):
            element[keyList[i]] = "${:0.2f}".format(basePrices[keyList[i]]*multiplier)

    else:
        for i in range(len(basePrices.keys())):
            element[keyList[i]] = "Out Of Area"


    data['Prices']=element
    return data



app = Klein()
@app.route("/Prices/<int:zip>")
def serve(request,zip):
    request.setHeader('Access-Control-Allow-Origin', '*')
    request.setHeader('content-type', 'application/json')

    data = LookUpZip(zip)

    data = json.dumps(data)
    return data


app.run('0.0.0.0',port)