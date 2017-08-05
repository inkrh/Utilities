import json
import os
import sqlite3
import sys
import translitcodec
# import dataset
# import jwt
import unidecode
from klein import Klein
from collections import Counter
from twisted.internet import threads
import string
from PIL import Image
import io

privateKeyPath = 'privkey.pem'
certificatePath = 'cert.pem'

debug = "DEBUG"
release = "RELEASE"
test = "TEST"
##POI
poiDB = "combinedPOI.db"


def ConvertCoordToZ9(x, z):
    return (x / (pow(2., z))) * (pow(2., 9))


def ConvertCoordsToZ9(x, y, z):
    return (ConvertCoordToZ9(x, z), ConvertCoordToZ9(y, z))


def SizeDiff(z):
    return (pow(2., z)) / (pow(2., 9))


def runQuery(cur, command):
    # print("Running : " + command)
    cur.execute(command)
    return cur.fetchall()


def RiseFact(v):
    con = sqlite3.connect(poiDB)
    cur = con.cursor()

    if v>-1:
        r = runQuery(cur,"select * from SeaLevelFacts where Level=="+str(v))
    else:
        r = runQuery(cur,"select * from SeaLevelFacts")

    data = {}
    levelinfo = []
    for item in r:
        element = {"Level":item[0],"Fact":item[1]}
        levelinfo.append(element)
    data["SeaLevelFacts"]=levelinfo
    con.close()
    json_data = json.dumps(data)
    return json_data


def decode(s):
    table = translitcodec.long_table
    return s.translate(table)


def sanitizeString(s):
    # s = unicode(s)
    s = decode(s)
    o = ""
    for i in range(0,len(s)):
        if s[i] in '"\',':

            if i == 0:
                o = o + "\"" + s[i]
            else:
                if not s[-i] == "\"":
                    o= o + "\"" + s[i]
        else:
            o = o + s[i]

    ##catchall
    return unidecode.unidecode(s)


def LandslideCharReplacement(s):
    s =s.replace('A(c)','e').replace('AS',"\'").replace(' _ '," - ").replace('_',' ').\
        replace('A3','o').replace('A*','\'').replace('uA','ui').replace('A+-','n').replace('RAo','Rio').\
        replace('hAc','hic').replace('A!','a').replace('aAd','aid').replace('aEUR(tm)',"\'").replace('aEURoe',"\'")
    s= s.replace('aEUR',"\'").replace("A'","\'").replace('A"',"\'").replace(' e Copyright',' Copyright').replace('AA ', 'A ').replace('\'"',"\'")\
    .replace(" paAs ", " pais ").replace("ayAoa","ayua").replace("[?]degn","an").replace("Juay[?][?]a","Juayua").replace("Enr[?][?]quez","Enriquez")
    return s



def LandslideJson():
    with open("landslides.json") as data_file:
        data = json.load(data_file)
    return data

def GenericizeLandslideData(data, minX, minY, maxX, maxY):
    poi = []
    try:
        for i in data:
            if "near" in i.keys():
                name = LandslideCharReplacement(unidecode.unidecode(i["near"]))

                element = {"Name": name+ " "+i["id"], "Type": "L", "Shape": "Point", "Lat": float(i["latitude"]),
                           "Lon": float(i["longitude"]),
                           "Points": [[float(i["latitude"]), float(i["longitude"])]]}

                ##large variation in what is in each json element
                landslidesize =""
                landslidetype =""
                if "landslide_size" in i.keys():
                    landslidesize = LandslideCharReplacement(i["landslide_size"].title()) + " "
                if "landslide_type" in i.keys():
                    landslidetype = LandslideCharReplacement(i["landslide_type"]) + "\n"
                elif "hazard_type" in i.keys():
                    landslidetype = i["hazard_type"] + "\n"

                element["Content"] = unidecode.unidecode(landslidesize + landslidetype)+name+'\n'

                if "comments" in i.keys():
                    element["AdditionalContent"] = LandslideCharReplacement(unidecode.unidecode(i["comments"]))
                else:
                    element["AdditionalContent"] = ""
                if "source_link" in i.keys():
                    element["URL"] = i["source_link"]
                else:
                    element["URL"]=""

                element["Organization"] = 4
                ##have to process anyway to get the values so doing this here
                if element["Lat"] >= minX and element["Lat"] <= maxX and element["Lon"] >= minY and element["Lon"] <= maxY:
                    poi.append(element)
    except:
        print("Error decoding landslide json")

    return poi


def NasaJson():
    with open('nasaEvents.json') as data_file:
        data = json.load(data_file)
    return data


def GenericizeNasaData(data, minX, minY, maxX, maxY):
    events = data['events']
    poi = []
    try:

        for i in events:
            name = sanitizeString(i['title'])


            element = {"Name": name, "Type": "N"}
            if len(i["geometries"]) >0:
                if i["geometries"][0]["type"] == 'Point':
                    element["Shape"] = "Point"
                    element["Lat"] = i["geometries"][0]["coordinates"][1]
                    element["Lon"] = i["geometries"][0]["coordinates"][0]
                    element["Points"] = [[i["geometries"][0]["coordinates"][1],i["geometries"][0]["coordinates"][0]]]
                elif i["geometries"][0]["type"] == "Polygon":
                    element["Shape"] = "Polygon"
                    element["Lat"] = i["geometries"][0]["coordinates"][0][0][1]
                    element["Lon"] = i["geometries"][0]["coordinates"][0][0][0]
                    points = []
                    for j in i["geometries"][0]["coordinates"]:
                        for p in j:
                            points += [[p[1], p[0]]]
                    element["Points"]=points


                content = "NASA Warnings" + "\n"
                element["Content"] = content + sanitizeString(i["categories"][0]["title"])
                element["AdditionalContent"] = sanitizeString(i["description"])
                element["URL"] = sanitizeString(i["sources"][0]["url"])
                element["Organization"] = 4
                ##have to process anyway to get the values so doing this here
                if element["Lat"] >= minX and element["Lat"] <= maxX and element["Lon"] >= minY and element["Lon"] <= maxY:
                    poi.append(element)
    except:
        print("Error decoding nasa json")
    return poi


##alert == the text string of the alert
##organization == organization ID
##lat,lon == location for alert, continual if empty
def AddAlert(alert,organization, lat,lon):
    con = sqlite3.connect(poiDB)
    cur = con.cursor()
    q = "insert into Alerts values (?,?,?,?)"
    cur.execute(q,(alert,organization,lat,lon))
    con.commit()
    con.close()

def Alert(all=True,lat=0,lon=0):

    con = sqlite3.connect(poiDB)
    cur = con.cursor()
    if all:
        q = "select * from Alerts"
    else:
        q = "select * from Alerts where Lat > " + str(lat-1) + " and Lat < " + str(lat+1) + " and Lon > " + str(lon-1) + " and Lon < " +str(lon+1)

    cur.execute(q)
    results = cur.fetchall()
    data = {}
    alerts = []
    if len(results)>0:
        for item in results:
            element = {"Alert": item[0],"Organization": item[1], "Lat": item[2], "Lon": item[3]}
            alerts.append(element)
    data["Alerts"] = alerts
    con.close()
    json_data = json.dumps(data)
    return json_data

##server -serving POI json
def queryDB(POItype):
    con = sqlite3.connect(poiDB)
    cur = con.cursor()
    data = {}

    if POItype == "N":
        if os.path.isfile("nasaEvents.json"):
            data['Locations'] = GenericizeNasaData(NasaJson())
    elif POItype=="L":
        if os.path.isfile("landslides.json"):
            data["Locations"] = GenericizeLandslideData(LandslideJson(),-90,-180,90,180)
    else:
        results = runQuery(cur, "select * from LOCATIONS where Type='" + POItype + "'")

        location = []
        for item in results:
            detailresults = runQuery(cur, "select * from DETAIL where Name='" + str(item[0]) + "'")
            for detailitem in detailresults:
                element = {"Name": sanitizeString(item[0]), "Type": sanitizeString(item[1]), "Lat": item[2],
                           "Lon": item[3], "Content": sanitizeString(detailitem[1]),
                           "AdditionalContent": sanitizeString(detailitem[2]), "URL": sanitizeString(detailitem[3])}
                org = 0
                if type(detailitem[4]) == int:
                    org = detailitem[4]
                element["Organization"] = org
                location.append(element)

        data['Locations'] = location
    con.close()
    json_data = json.dumps(data)
    return json_data


def queryDBByLocation(minX, minY, maxX, maxY):
    con = sqlite3.connect(poiDB)
    cur = con.cursor()
    results = runQuery(cur,
                       "select * from LOCATIONS where Lat>" + str(minX) + " and Lat<" + str(maxX) + " and Lon>" + str(
                           minY) + " and Lon <" + str(maxY))
    data = {}
    location = []

    for item in results:
        # print(item[0])
        cur.execute('select * from DETAIL where Name="'+item[0]+'"')
        detailresults = cur.fetchall()
        # detailresults = runQuery(cur, "select * from DETAIL where Name='" + str(item[0]) + "'")
        for detailitem in detailresults:
            element = {"Name": sanitizeString(item[0]), "Type": sanitizeString(item[1]), "Lat": item[2], "Lon": item[3],
                       "Shape": "Point","Points":[[item[2],item[3]]],
                       "Content": sanitizeString(detailitem[1]), "AdditionalContent": sanitizeString(detailitem[2]),
                       "URL": sanitizeString(detailitem[3])}
            org = 0
            if type(detailitem[4]) == int:
                org = detailitem[4]
            element["Organization"] = org
            location.append(element)

    if os.path.isfile("nasaEvents.json"):
        try:
            location += GenericizeNasaData(NasaJson(), minX, minY, maxX, maxY)
        except:
            print("Error in Nasa Data Json")

    if os.path.isfile("landslides.json"):
        try:
            location += GenericizeLandslideData(LandslideJson(), minX, minY, maxX, maxY)
        except:
            print("Error in Landslides Data Json")
    con.close()

    data['Locations'] = location
    json_data = json.dumps(data)
    return json_data


def OrganizationData(results):
    data = {}
    organization = []
    if len(results) >= 0:
        for item in results:
            element = {"ID": item[0], "NAME": sanitizeString(item[1])}

            if type(item[2]) is None:
                element["DONATE"] = ""
            else:
                element["DONATE"] = sanitizeString(item[2])
            if type(item[3]) is None:
                element["INVOLVE"] = ""
            else:
                element["INVOLVE"] = sanitizeString(item[3])
            element["ABOUT"] = sanitizeString(item[4])
            organization.append(element)
    data['Organizations'] = organization
    return data


def queryDBTypes():
    con = sqlite3.connect(poiDB)
    cur = con.cursor()
    results = runQuery(cur, "select * from Types")
    con.close()
    data = {}
    types = []

    if len(results)>0:
        for item in results:
            element = {"Type":item[0],"Icon":item[1],"Description":item[2]}
            types.append(element)

    data["Types"] = types

    return json.dumps(data)


def queryDBAllOrganizations():
    con = sqlite3.connect(poiDB)
    cur = con.cursor()
    results = runQuery(cur, "select * from ORGANIZATIONS")
    data = OrganizationData(results)
    json_data = json.dumps(data)
    con.close()
    return json_data


def queryDBByOrganization(id):
    con = sqlite3.connect(poiDB)
    cur = con.cursor()
    results = runQuery(cur, "select * from ORGANIZATIONS where ID=" + str(id))
    data = OrganizationData(results)
    json_data = json.dumps(data)
    con.close()
    return json_data

def queryDBByName(name):
    con = sqlite3.connect(poiDB)
    cur = con.cursor()
    name = str(name).lower()
    results = runQuery(cur, "select * from DETAIL where Name like '%"+name+"%'")
    data = {}
    locations = []
    if len(results)>0:
        for item in results:
            element = {"Name": sanitizeString(item[0]),
                       "Content": sanitizeString(item[1]), "AdditionalContent": sanitizeString(item[2])}
            locations.append(element)
    data['Locations'] = locations
    json_data = json.dumps(data)
    return json_data


#
# def validateRequest(request):
#     encoded = request.getHeader('Authorization')
#     payload = jwt.decode(encoded, verify=False)
#     email = sanitizeString(payload['email'])
#     secret = getUserSecret(email)
#     if secret is not None:
#         decoded = jwt.decode(encoded, secret, algorithm='HS256')
#         if decoded is not None:
#             return True
#         else:
#             return False
#     else:
#         return False
#
#
# def getUserSecret(em):
#     db = dataset.connect('sqlite:///users.db')
#     table = db['users']
#     user = table.find_one(email=em)
#     if user is not None:
#         return user['secret']
#     else:
#         return None

def jsonCallBack(j):
    return j

def poiIcon(filename):
    filename = os.path.join("poiicons",filename)
    return Image.open(filename)


def ImgCallBackBytes(img):
    imgBytes = io.BytesIO()
    img.save(imgBytes, format='PNG')
    imgBytes = imgBytes.getvalue()
    # return str(imgBytes)
    return imgBytes


app = Klein()

@app.route("/Types",branch=True)
def getTypes(request):
    global tgT
    request.setHeader('content-type','application/json')
    tgT = threads.deferToThread(queryDBTypes)
    return tgT.addCallback(jsonCallBack)

@app.route("/Icon/<string:name>",branch=True)
def getIcon(request,name):
    global igI
    try:
        request.setHeader('content-type', 'image/png')
        igI = threads.deferToThread(poiIcon,name)
        return igI.addCallback(ImgCallBackBytes)

    except:
        print(name + "issue")

    return ""


# POItype - C/E/R/G
@app.route("/POI/<string:POItype>", branch=True)
def getPOI(request, POItype):
    global dgp
    if not mode == test:
        request.setHeader('content-type', 'application/json')
    ##check combinedPOI.db
    ##return json with type
    dgp = threads.deferToThread(queryDB,POItype)
    return dgp.addCallback(jsonCallBack)

@app.route("/POIByName/<string:name>", branch=True)
def getPOIByName(request,name):
    if string.punctuation in name:
        for c in string.punctuation:
            name = name.replace(c,' ')

    name = name.lower()
    name = name.replace(';',' ').replace('update',' ').replace('drop',' ').replace('create',' ').replace('delete',' ')
    name = name.replace('"',' ').replace("'",' ')
    name = name.replace('_',' ')
    name = name.replace("insert", ' ')
    name = name.replace(' into ',' ')
    name = name.replace(' select ',' ')
    name  = name.replace('table', ' ')
    if len(name.strip()) <= 0:
        return ''
    global gpbyn
    request.setHeader('Access-Control-Allow-Origin', '*')

    request.setHeader('content-type', 'application/json')
    gpbyn = threads.deferToThread(queryDBByName,name.strip())
    return gpbyn.addCallback(jsonCallBack)

# POI by bounds
@app.route("/POIByBounds/<string:minX>/<string:minY>/<string:maxX>/<string:maxY>", branch=True)
def getPOIByBounds(request, minX, minY, maxX, maxY):
    global dpbb
    try:
        minX = float(minX)
        minY = float(minY)
        maxX = float(maxX)
        maxY = float(maxY)
    except:
        print("Argument exception")
        return ""

    if not mode == test:
        request.setHeader('content-type', 'application/json')
    ##check combinedPOI.db
    ##return json with type
    dpbb = threads.deferToThread(queryDBByLocation,minX,minY,maxX,maxY)
   ## return queryDBByLocation(minX, minY, maxX, maxY)
    return dpbb.addCallback(jsonCallBack)


@app.route("/Alerts/<string:lat>/<string:lon>",branch=True)
def getSpecificAlerts(request,lat,lon):
    latint = 0
    lonint=0
    try:
        latint = float(lat)
        lonint = float(lon)
    except:
        return getAllAlerts(request)

    global allAlerts
    if not mode == test:
        request.setHeader('content-type','application/json')

    allAlerts = threads.deferToThread(Alert,False,latint,lonint)
    return allAlerts.addCallback(jsonCallBack)



@app.route("/Alerts",branch=True)
def getAllAlerts (request):
    global allAlerts
    if not mode == test:
        request.setHeader('content-type','application/json')
    allAlerts = threads.deferToThread(Alert)
    return allAlerts.addCallback(jsonCallBack)



@app.route("/Organization/<string:id>", branch=True)
def getOrganization(request, id):
    global dgo
    try:
        id = int(id)
    except:
        id = -1
    ##should only be one organization, but can handle multiple organizations under same id
    if not mode == test:
        request.setHeader('content-type', 'application/json')
    dgo = threads.deferToThread(queryDBByOrganization,id)
    return dgo.addCallback(jsonCallBack)
  #  return queryDBByOrganization(id)




@app.route("/SeaLevelFacts/<string:level>", branch=True)
def getSeaLevelFacts(request,level):

    global dslf
    request.setHeader('content-type', 'application/json')


    try:
        level = int(level)
    except:
        return ""

    dslf = threads.deferToThread(RiseFact,level)
    return dslf.addCallback(jsonCallBack)
#    return RiseFact(level)



@app.route("/Organizations/", branch=True)
def getOrganizations(request):
    global dgos
    if not mode == test:
        request.setHeader('content-type', 'application/json')
    dgos = threads.deferToThread(queryDBAllOrganizations)
    return dgos.addCallback(jsonCallBack)
#    return queryDBAllOrganizations()


@app.route("/News", branch=True)
def getNews(request):
    request.setHeader('content-type', 'application/json')
    ##allow re-use of this in other sites (e.g. socialengine)
    request.setHeader('Access-Control-Allow-Origin', '*')
    ##read hourly updated json file with news articles
    if os.path.isfile("feedData.json"):
        with open("feedData.json") as o:
            return o.read()
    else:
        return ""


@app.route("/NasaJson", branch=True)
def getNasaJson(request):
    request.setHeader('content-type', 'application/json')
    ##allow re-use of this in other sites (e.g. socialengine)
    request.setHeader('Access-Control-Allow-Origin', '*')
    ##read hourly updated json file with nasa events
    if os.path.isfile("nasaEvents.json"):
        with open("nasaEvents.json") as o:
            return o.read()
    else:
        return ""


@app.route("/")
def testConnection(request):
    return None


resource = app.resource
mode = release

https = False

for v in sys.argv:
    if v.lower() == "test":
        mode = test
    if v.lower() == "debug":
        mode = debug
    if v.lower() == 'https':
        https = True

endpointdesc = 'ssl:8084:privateKey=' + privateKeyPath + ':certKey=' + certificatePath
if not https:
    endpointdesc = ''

if mode == test:
    print("Testing mode, no server running.")
    print("to start server: app.run(<local/0.0.0.0>',<port>)")
##local test
elif mode == debug:
    print("Running on localhost")
    app.run('localhost', 8084, endpoint_description=endpointdesc)
##release
elif mode == release:
    print("Running on 0.0.0.0")
    app.run('0.0.0.0', 8084, endpoint_description=endpointdesc)


