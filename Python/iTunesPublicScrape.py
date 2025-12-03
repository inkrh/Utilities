import requests, json

"""
    Useful:
    https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/UnderstandingSearchResults.html
"""
publicstoredata = {}

# official public rating, country specific
def getpublicInfo(appId, iso2code="US"):
    r = requests.get("http://itunes.apple.com/lookup?id={id}&country={iso}".format(id=appId,iso=iso2code), auth=False)
    if r.status_code == 200:
        publicstoredata[appId] = r.json()
        with open("{app}{iso}.json".format(app=appId,iso=iso2code),'w') as o:
            json.dump(r.json(),o)
        return publicstoredata[appId]
    return ""

#show first result
def showFirstResult(appId,iso2code):
    if appId not in publicstoredata.keys():
        if getpublicInfo(appId,iso2code) == "":
            return "Not found"
    if "results" in publicstoredata[appId].keys() and publicstoredata[appId]["resultCount"] >0:
        return publicstoredata[appId]["results"][0]
    
