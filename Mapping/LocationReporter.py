import sqlite3
from klein import Klein
import datetime
import json


##Location recorder - returns available/!available and last location of user
##a little messy but is just a quick demo POC to stub out a server, several missing pathways (e.g. add/delete user delete location point etc.)
##also missing things such as decent threading and DB file handling, etc. and doing things like using GET for POSTing data

dblocation = "Locations.db"
ip = 'localhost'
port = 8080

def GetUserIDFromName(name):
    con = sqlite3.connect(dblocation)
    cur = con.cursor()
    cur.execute("select * from User where User.Name='"+name+"'")
    r=cur.fetchall()
    con.close()
    if len(r) <=0:
        return -1

    return r[0][0]


def LocationIn(user, lat,lon):
    ##double check lat/lon are floats
    if not type(lat)==float or not type(lon)==float:
        try:
            lat = float(lat)
            lon = float(lon)
        except:
            return -1

    t = DateTimeNowToString()

    con = sqlite3.connect(dblocation)
    cur = con.cursor()
    cur.execute('replace into Location values (?,?,?,?)',(user, lat,lon,t))
    con.commit()
    con.close()
    return 0


def LocationOut(user):
    con = sqlite3.connect(dblocation)
    cur = con.cursor()
    cur.execute('select * from Location where Id = '+str(user))
    r = cur.fetchall()
    con.close()
    if len(r)>0:
        ##could be neater but was lazy
        lasttime = StringToDateTime('20170101010101')
        timedata = 0
        lat = 0
        lon = 0
        for item in r:
            t = StringToDateTime(item[3])
            if t>lasttime:
                lasttime = t
                timedata = item[3]
                lat = item[1]
                lon = item[2]
        if lasttime > StringToDateTime('20170101010101'):
            return user,lat,lon,timedata
    return -1

def DateTimeNowToString():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')

def StringToDateTime(timeString):
    return datetime.datetime.strptime(timeString, '%Y%m%d%H%M%S')


def Put(user,lat,lon):
    id = GetUserIDFromName(user)
    if not id == -1:
        return LocationIn(id,lat,lon)

    return -1

def Fetch(user):
    if FetchAvailable(user):
        id = GetUserIDFromName(user)
        if not id == -1:
            return LocationOut(id)

    return -1


def PutAvailable(user,available):
    if not type(available)==bool:
        return -1

    id = GetUserIDFromName(user)
    if not id == -1:
        con = sqlite3.connect(dblocation)
        cur = con.cursor()
        cur.execute("replace into User values (?,?,?)",(id,user,int(available)))
        con.commit()
        con.close()
        return 0
    return -1

def FetchAvailable(user):
    id = GetUserIDFromName(user)
    if not id == -1:
        con = sqlite3.connect(dblocation)
        cur = con.cursor()
        cur.execute("select * from User where Id ==" + str(id))
        r =  cur.fetchall()
        con.close()
        if len(r)>0:
            if r[0][2]==1:
                return True
            return False

    return -1

def JSONResult(data):
    return json.dumps({"Lat":data[1],"Lon":data[2], "Time":data[3]})

app = Klein()

##lat/lon as strings to handle floats
@app.route("/Location/<string:name>/<string:lat>/<string:lon>")
def SetLocation(request,name,lat,lon):
    result = Put(name,lat,lon)
    if result == 0:
        request.setResponseCode(204)
    else:
        request.setResponseCode(400)
    return ""

@app.route("/Location/<string:name>")
def GetLocation(request,name):
    result = Fetch(name)
    if result == -1:
        request.setResponseCode(400)
        return ""
    request.setResponseCode(200)
    request.setHeader('content-type','application/json')
    return JSONResult(result)


@app.route("/Available/<string:name>/<int:available>")
def SetAvailable(request,name,available):
    if available == 1:
        available = True
    else:
        available = False

    result = PutAvailable(name,available)
    if result == 0:
        request.setResponseCode(204)
    else:
        request.setResponseCode(400)
    return ""

@app.route("/Available/<string:name>")
def GetAvailable(request,name):
    result = FetchAvailable(name)
    if result == -1:
        request.setResponseCode(400)
        return ""

    request.setResponseCode(200)
    request.setHeader('content-type','application/json')
    return json.dumps({'Available': str(result)})


app.run(ip,port)