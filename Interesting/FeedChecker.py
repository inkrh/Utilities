##relies on feedparser - pip install feedparser
##relies on unidecode - pip install unidecode

import feedparser
import string
import json
from unidecode import unidecode
import re, cgi
import sqlite3
import datetime

FeedList = {
    "BBC News":"http://feeds.bbci.co.uk/news/rss.xml",
    "BBC Environment":"http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "BBC World News":"http://feeds.bbci.co.uk/news/world/rss.xml",
    "Google":"http://news.google.com/news?output=rss",
    "BBC UK News":"http://feeds.bbci.co.uk/news/uk/rss.xml",
    "BBC US News":"http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml",
    "BBC Middle East News":"http://feeds.bbci.co.uk/news/world/middle_east/rss.xml",
    "CNN Top Stories":"http://rss.cnn.com/rss/cnn_topstories.rss",
    "CNN World News":"http://rss.cnn.com/rss/cnn_world.rss",
    "CNN US News":"http://rss.cnn.com/rss/cnn_us.rss",
    "News24":"http://feeds.news24.com/articles/News24/Technology/rss",
    "WWF":"http://feeds.feedburner.com/WWFStories?format=xml",
    "WWF In News":"http://feeds.feedburner.com/WWF-InTheNews?format=xml",
    "Guardian":"http://www.theguardian.com/rss"
    }

##TODO use a configuration file for more common words

KeyPhrases= ["climate change","global warming", "environment","climatechange",
             "sea level", "energy","temperature","climate", "species", "smog",
             "pollution","flood","extinct","oil pipe", "extinct", "air quality"]

CommonWords = []

Blacklist = ['clickbait','how can', 'are you', 'asylum seeker', 'what I wore this week','quits crisps','northern ireland assembly','fashion']


def replaceNonAlphanumeric(s):
    o = ""
    for l in s:
        if l in string.ascii_letters or l in string.digits or l in " " or l in "'":
            o=o+l
        elif l in string.punctuation:
            o = o + " "

    o = o.replace("  "," ")
    
    return o

def replaceCommonWords(s):
    for word in CommonWords:
        s = s.replace(" "+word+" "," ")
    s = s.replace("  "," ")
    return s

def selectArticle(feedURL):
    feed = feedparser.parse(feedURL)

    for entry in feed.entries:
        print(str(feed.entries.index(entry)) + " : " + entry.title)

    if len(feed.entries)<=0:
        return None
    
    entryNumber = int(input ("Choose an article to score : "))
    return feed.entries[entryNumber]

def selectFeed():
    i = 1
    f = []
    for k,v in FeedList.iteritems():
        print(str(i)+ " : " + k)
        f.append(k)
        i+=1
    chosenFeed = input("Choose a feed : ")
    return f[int(chosenFeed)-1]

def Search():
    CurrentStories = []
    for k,v in FeedList.iteritems():
        f = feedparser.parse(v)
        for entry in f.entries:
            t = entry.title
            e = stripTags(entry.description)
            l = entry.link
            if CheckWords(t) or CheckWords(e):
                CurrentStories.append((t,e,l))
    return CurrentStories

def Run():
    results = Search()
    if len(results)>0:
        o = open("feedData.json",'w')
        data = {}
        feed = []
        d = str(datetime.datetime.now().ctime())

        for item in results:
            element = {}
            element["Title"] = sanitizeString(item[0])
            element["Description"] = sanitizeString(item[1])
            element["URL"] = sanitizeString(item[2])
            feed.append(element)
            AddToDB(sanitizeString(item[0],True),sanitizeString(item[1],True),sanitizeString(item[2],True),d)
        data['feeds'] = feed
        json_data = json.dumps(data)
        o.write(json_data)
        o.close()
#        print("Rewrote feeds with "+ str(len(results))+" articles.")
#    else:
#        print("No new feeds")
    
def CheckWords(target):
    t = target.lower()
    r = False
    ##remove blacklist items
    for item in Blacklist:
        if item.lower() in t.lower():
            return False

    for item in KeyPhrases:
        if item.lower() in t.lower():
            r = True

    return r

def sanitizeString(s, singles=False):
    s = unidecode(s)
    s = str(s).encode('utf-8','ignore').replace('"'," ").replace(',',' ')
    if singles:
        s = s.replace("'","")
    return s

#    print(str(i.count(True)) + " : " +str(len(it)))
    f = float(i.count(True)/len(it))
    return f

##add to db
def AddToDB(title,description,url, d):
    con = sqlite3.connect("FeedHistory.db")
    cur = con.cursor()
    q = "INSERT INTO FeedHistory VALUES ('"+title+"','"+description+"','"+url+"','"+d+"')"
    cur.execute(q)
    con.commit()
    con.close()
    
##from stack overflow
def stripTags(raw_html):
  cleanr = re.compile('<.*?>')
  cleanescapes = re.compile('&.*?;')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = re.sub(cleanescapes,' ',cleantext)
  return cleantext


Run()
