import json
import os
import sqlite3
import sys
from klein import Klein
from twisted.internet import threads
from twisted.web.util import redirectTo


appTargetDB = "apps.db"
columns=["id","android","ios"]

def runQuery(cur, command):
    # print("Running : " + command)
    cur.execute(command)
    return cur.fetchall()


def querydb(term,platform):
    con = sqlite3.connect(appTargetDB)
    cur = con.cursor()
    results = runQuery(cur, "select "+platform+" from apps where id='"+term+"'")
    print(results)
    data = {}
    searchResults = []
    if len(results)>0:
        return json.dumps(results[0][0])
    return ""

app = Klein()

@app.route("/app/<string:name>", branch=True)
def getRightLink(request,name):
    print(name)
    global cb
    ua = request.getHeader("user-agent")
    tp="ios"
    if "android" in ua:
        tp="android"
    print(querydb(name,tp))
    return redirectTo(querydb(name,tp),request)

        

@app.route("/")
def testConnection(request):
    return None

endpointdesc = ''
app.run('localhost', 9090, endpoint_description=endpointdesc)
