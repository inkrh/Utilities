import json
import sqlite3
import sys
import translitcodec
import unidecode
from klein import Klein
from PIL import Image
import io

privateKeyPath = 'privkey.pem'
certificatePath = 'cert.pem'

debug = "DEBUG"
release = "RELEASE"
test = "TEST"
rewardsDB = "RewardsRedux.db"
quizDB = "quizDB.db"
rewardsRoot = "Rewards/"

def GetRewardsImage(n,theme,width,height):
    r = GetThemesRewards(theme)
   ## print(len(r))
    if len(r)>0:
      ##  print(n%len(r))
        n = n%len(r)
        result = r[n]

        fn = rewardsRoot+result["Name"]
        img = Image.open(fn)
        img = Resize(img,width,height)
        with Image.open(fn) as img:
            imgBytes = io.BytesIO()
            img.save(imgBytes, format='PNG')
            imgBytes = imgBytes.getvalue()
            return imgBytes
    return ""

def Resize(img,width,height):
    oldMode = img.mode
    w,h = img.size

    if width < w or height < h:
        aspectw = float(width)/w
        aspecth = float(height)/h
        ratio = min(aspectw,aspecth)
        img = img.resize((int(w*ratio),int(h*ratio)))
        w,h = img.size

    if not oldMode == 'RGBA':
        img = img.convert('RGBA')

    bg = Image.new('RGBA',(width,height))
    nx = (width/2)-(w/2)
    ny = (height/2)-(h/2)
    return ImageMerge(img,bg,nx,ny).convert(oldMode)

def ImageMerge(i1, i2,x,y):
    r, g, b, a = i1.split()
    t = Image.merge("RGB", (r, g, b))
    m = Image.merge("L", (a,))
    i2.paste(t, (int(x), int(y)), m)
    return i2




def GetThemesRewards(id):
    recon = sqlite3.connect(rewardsDB)
    recur = recon.cursor()
    results = runQuery(recur,"select * from Rewards where Theme =="+str(id))
    if len(results)<=0:
        results = runQuery(recur,"select * from Rewards")
    rewards = []
    for item in results:
        element = {}
        element["Theme"] = item[0]
        element["Name"] = item[1]
        rewards.append(element)
    return rewards


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



def runQuery(cur, command):
    ##    print("Running : " + command)
    cur.execute(command)
    return cur.fetchall()


def FetchThemes():
    global cur
    ##uncomment to get all themes - handy for testing UI
    ##results = runQuery(cur,"select * from Themes")
    ##otherwise just get themes which have questions
    results = runQuery(cur,"select * from Themes where Themes.ID in (select distinct Questions.Theme from Questions)")
    data = {}
    themes = []
    for item in results:
        element = {"ID": item[0],"Theme":item[1]}
        themes.append(element)
    data["Quizzes"] = themes
    return json.dumps(data)

def FetchQuestions(theme):
    global cur
    data = {}
    quiz = []
    results = runQuery(cur, "select * from Questions where Theme=="+str(theme))
    for item in results:
        answers = [sanitizeString(item[1]),sanitizeString(item[2]),sanitizeString(item[3]),sanitizeString(item[4])]
        element = {"Question":sanitizeString(item[0]),"Answers":answers, "Correct":sanitizeString(item[1])}
        quiz.append(element)
    data["Questions"] = quiz
    return json.dumps(data)

app = Klein()

@app.route("/Questions/<int:id>", branch=True)
def getThemeQuestions(request, id):
    request.setHeader("content-type","application/json")
    return FetchQuestions(id)

@app.route("/Themes", branch=True)
def getThemes(request):
    request.setHeader("content-type", "application/json")
    return FetchThemes()

@app.route("/Reward/<int:id>/<int:theme>/<int:width>/<int:height>", branch=True)
def getReward(request,id,theme,width,height):
    request.setHeader('content-type', 'image/png')
    return GetRewardsImage(id,theme,width,height)




global con,cur

resource = app.resource
mode = release
https = False

with sqlite3.connect(quizDB) as con:

    cur = con.cursor()

    for v in sys.argv:
        if v.lower() == "test":
            mode = test
        if v.lower() == "debug":
            mode = debug
        if v.lower() == 'https':
            https = True

    endpointdesc = 'ssl:8086:privateKey=' + privateKeyPath + ':certKey=' + certificatePath

    if not https:
        endpointdesc = ''


    ##source control has POI db in different folder
    if mode == test:
        print("Testing mode, no server running.")
        print("to start server: app.run(<local/0.0.0.0>',<port>)")
    ##local test
    elif mode == debug:
        print("Running on localhost")
        app.run('localhost', 8086, endpoint_description=endpointdesc)
    ##release
    elif mode == release:
        print("Running on 0.0.0.0")
        app.run('0.0.0.0', 8086,endpoint_description=endpointdesc)

con.close()
