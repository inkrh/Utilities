import json
import sqlite3

##fix bad json formatting in data as received from FEMA
def FemaJsonClean():

    with open('cleanFema.json','w') as of:
        of.write('[')
        with open('femaEvents.json') as df:
            for line in df:
                o = line
                if '}{' in line:
                    o = line.replace('}{','},{')
                of.write(o)
        of.write(']')

##return clean FEMA data
def FemaJson():
    with open('cleanFema.json') as data_file:
        data = json.load(data_file)
    return data


##establish a point from the county, state text
def GetLatLonFromCountyState(county,state):
    if len(county)>1:
        if '(' in county:
            county = county[0:county.find('(')]
        county = county.strip()
        state = state.strip()
        county = county[0]+county[1:].lower()
        county = county.title()
        zdb = sqlite3.connect('CountyLocationLookup.db')
        zdbcur = zdb.cursor()
        q= 'select * from zip_codes_states where county == "'+county+'" and state == "'+state+'"'
        # print(q)
        zdbcur.execute(q)
        r = zdbcur.fetchall()
        zdbcur.close()

        if len(r) > 0:
            lat = float(r[0][1])
            lon = float(r[0][2])
            if len(r) > 1:
                for item in r[1:len(r)]:
                    lat = lat + float(item[1])
                    lon = lon + float(item[2])
                lat = float(lat/len(r))
                lon = float(lon/len(r))
            return lat,lon
    return -1


##clean up and put in our format
def GenericizeFemaData(data):

    con = sqlite3.connect("FEMA.db")
    cur = con.cursor()
    try:
        for line in data:
            # if line['declarationDate'].startswith("2017"):
            element = {"Name": line['incidentType'], "Content": line['title']}
            #element["Organization"] = 5

            ac = ""
            if 'declaredCountyArea' in line.keys() and 'state' in line.keys():
                ac = line['declaredCountyArea'] + ", " + line['state'] + "\n"
            year = 9999
            if 'incidentBeginDate' in line.keys():
                ac = ac + line['incidentBeginDate'][0:10]

                if line['incidentBeginDate'][0:4].isdigit():
                    year = int(line['incidentBeginDate'][0:4])
                if 'incidentEndDate' in line.keys():
                    ac = ac + " - " + line['incidentEndDate'][0:10]

            element['Year'] = year

            element['AdditionalContent']= ac

            p = GetLatLonFromCountyState(line['declaredCountyArea'],line['state'])
            if not p==-1:
                ##print(p[0],p[1])
                element["Lat"] = p[0]
                element["Lon"] = p[1]
                element["ID"] = line['id']
                # print(element)
                cur.execute('replace into FEMA values (?,?,?,?,?,?,?)',(element ['ID'],element['Lat'], element['Lon'], element['Name'], element['Content'], element['AdditionalContent'],element['Year']))
    except:
        print("Error inserting values into DB")

    con.commit()
    cur.close()
    con.close()

try:
    print("Cleaning source json")
    FemaJsonClean()
    print("Adding to DB")
    GenericizeFemaData(FemaJson())
    print("DONE")
except:
    print("Failed cleaning FEMA data")

