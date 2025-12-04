#! /usr/bin/python3

import csv
import translitcodec
import unidecode
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import socket
import sys
import os
from bs4 import BeautifulSoup

timeoutseconds=30
countryInCSV=False
makeCMDBSuggestions=False
headless=False

headers={ "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

fileTypesToFollow=['.js','.css','.txt','.php']

def printHeadless(s):
    if not headless:
        print(s)

def readCSV(filename):
#    returns JSON list of rows from CSV each is a dict
    global countryInCSV

    colnames=[]
    output=[]

    with open(filename,'r') as o:
        reader = csv.reader(o, delimiter=',')
        lc = 0
        
        for row in reader:
            rowDict={}
            if lc==0:
                for i in row:
                    colnames.append(i.replace("\xef\xbb\xbf",""))
            else:
                for i in row:
                    rowDict[colnames[row.index(i)]]=i.strip()
                
                output.append(rowDict)
            lc+=1
    if "Country" in colnames:
        countryInCSV=True
    return output

def cssAndJsCheck(htmlcontent, url):
    #TODO some sort of check to avoid having to check same file on different URLs
    #parse htmlcontent
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    #are there any style tags?
    outbound=[]
    outbound=outbound+soup.find_all('style', href=True)
    outbound=outbound+soup.find_all('link', href=True)
    outbound=outbound+soup.find_all('script')
    
    #what is js/css file location?
    toCheck=[]
    for f in outbound:
        for attr in f.attrs:
            if 'src' in attr or 'href' in attr:
                fixUrl=str(f[attr])
                #make absolute URL (only looking at the top page so should work, would need more if subpages)
                if not fixUrl.startswith("http"):
                        fixUrl=urljoin(url,fixUrl)
                #is in allowed file types, could also split on . and use last element, easier this way
                follow=False
                for ft in fileTypesToFollow:
                    if ft in fixUrl:
                        follow=True
                #only add if not added - some pages have the same css file referenced multiple times
                if follow and not fixUrl in toCheck:
                    toCheck.append(fixUrl)
    #GET files and search
  
    googlefont=False
    
    for endpoint in toCheck:
        printHeadless("Checking "+str(endpoint))
        session = requests.Session()
        session.trust_env = False
        thisheaders = headers
        thisheaders["Referrer"]=url
        
        r=session.get(endpoint,headers=thisheaders, verify=False, allow_redirects=False, timeout=timeoutseconds)
        #return first reference and break out of for loop - don't need to check more if we've found at least one
        if "fonts.googleapis.com" in str(r.content) or "fonts.gstatic.com" in str(r.content):
            checkcommented=str(r.content).split("fonts.googleapis.com")
            
            googlefont=True
            return " Google Fonts found in "+endpoint

    #if we get to this point the tool hasn't found anything in those files checked
    return ""

#admittedly from stackoverflow
def urljoin(*args):
    return "/".join(map(lambda x: str(x).rstrip('/').lstrip('/'), args))


def searchContent(content, url):
    #TODO replace this and iterate set of search keywords properly
    databack=""
    if "/wp/" in str(content) or "wp-" in str(content) or "wordpress" in str(content) or "yoast seo" in str(content):
        databack=databack+" Wordpress"
        
    if "fonts.googleapis.com" in str(content) or "fonts.gstatic.com" in str(content):
        databack=databack+" Google Fonts"
    
    return databack

def checkContent(r, protocol,url):
    databack=str(r.status_code) #fallback
    printHeadless(protocol+url)
    printHeadless(r.status_code)
    if r.status_code==200:
        
        ##TODO parse content properly to see if truly blank
        if len(r.content)<=94 or "body></body>" in str(r.content):
            databack="Blank Website: "+str(len(r.content))+" bytes returned"
        else:
            databack="Live Website: "+str(len(r.content))+" bytes returned"
            #search for content in main html
            databack=databack+searchContent(r.content.lower(), protocol+url)
           

            #check js and css files
            #don't need to check if already detected for site
            if "Google Fonts" not in databack:
                databack=databack+cssAndJsCheck(r.content.lower(), protocol+url)
    
    #redirect handling
    if r.status_code>=300 and r.status_code<=399:
        databack="A redirect: " + r.headers['Location']
        if r.status_code==301 or r.status_code==308:
            databack="Permanent redirect: " + r.headers['Location']
        if r.status_code==302 or r.status_code==307:
            databack="Temporary redirect: " + r.headers['Location']
        if r.status_code==303:
            databack="Other redirect: " + r.headers['Location']
        
        if r.headers['Location'].startswith("/") or url in r.headers['Location']:
            databack="Same site redirect: "+ r.headers['Location']
            
    
    
    
    if r.status_code>=500 and r.status_code<=599:
        databack="Error on server " + str(r.status_code)

    if r.status_code>=400 and r.status_code<=499:
        databack="Error on URL or request " + str(r.status_code)
        if r.status_code==404:
            databack=" Not Found " + str(r.status_code)
        if r.status_code==403 or r.status_code==401:
            databack=" Access Forbidden or Unauthorized: "+str(r.status_code)
        if r.status_code==406:
            databack=" Check manually "+str(r.status_code)
        
    return databack


def tryRequest(url,protocol):
    printHeadless(protocol)
    try:
        session = requests.Session()
        session.trust_env = False
        thisheaders = headers
        thisheaders["Referrer"]=protocol+url
        
        r=session.get(protocol+url,headers=thisheaders, verify=False, allow_redirects=False, timeout=timeoutseconds)
        
        databack=checkContent(r, protocol,url)

            
        
        if "redirect" in databack and (url in r.headers['Location'] or r.headers['Location'].startswith('/') or r.headers['Location'].startswith('/')):

            databack="Same domain redirect: "+r.headers['Location']
            new_url=r.headers['Location']
            printHeadless("Redirect location specified in headers : "+new_url)
            
            if r.headers['Location'].startswith('/') or r.headers['Location'].startswith('/'):
                new_url=protocol+url+r.headers['Location']
                
            burn=session.get(new_url,verify=False, allow_redirects=False, timeout=timeoutseconds)
            databack=checkContent(burn, "",new_url)
            
    except Exception as e:
    
        if "not known" in str(e):
            databack="Error Name Resolution Failed"
        elif "SSL" in str(e):
            databack="SSLError"
            if "ECONNRESET" in str(e):
                databack="SSLError Connection Reset"
        elif "timed out" in str(e):
            databack="TimeOutError"
        else:
            
            printHeadless(protocol+url + " Failed with " + str(e))
            databack=str("Error: "+str(e))
            
    if "Wordpress" in databack:
        if checkWordpressVIP(url):
            databack = databack+" VIP"
            
    printHeadless(databack)
    return databack

def checkWordpressVIP(url):
    ##check if hosted on the wordpress vip solution's IP
    ip=""
    try:
        ip = socket.gethostbyname(url)
        printHeadless(ip)
    except Exception as e:
        printHeadless("socket.gethostbyname failed on "+url+" with " + str(e))
        
    return ip.startswith('192.0.66')

def searchDictionaryKeyValuePartialMatch(d,value):
    return any([True for k,v in d.items() if value in v])
    
    
def dns_lookup(host,port):
    try:
        socket.getaddrinfo(host, port)
    except socket.gaierror:
        return False
    return True
    


def parseCSV(csvData):
    
    output=[]
    for i in csvData:
        print(i)
        print('URL' in i)
        if 'URL' in i:
                
            eachSiteOutputDict={}
            if countryInCSV and 'Country' in i:
                eachSiteOutputDict['Country']=i['Country']
            
            bestProtocolToScrape=""
            printHeadless("Working: " + i['URL'])
            os.environ['NO_PROXY']=i['URL']
            try:
                eachSiteOutputDict['http']=tryRequest(i['URL'],"http://")
                eachSiteOutputDict['httpwww']=tryRequest(i['URL'],"http://www.")
                eachSiteOutputDict['https']=tryRequest(i['URL'],"https://")
                eachSiteOutputDict['httpswww']=tryRequest(i['URL'],"https://www.")
                    
                LiveWebsite=searchDictionaryKeyValuePartialMatch(eachSiteOutputDict,"Live")
                BlankWebsite=searchDictionaryKeyValuePartialMatch(eachSiteOutputDict,"Blank")
                ErrorWebsite=searchDictionaryKeyValuePartialMatch(eachSiteOutputDict,"Error")
                RedirectedWebsite=searchDictionaryKeyValuePartialMatch(eachSiteOutputDict,"redirect")
                GoogleFonts=searchDictionaryKeyValuePartialMatch(eachSiteOutputDict,"Google Fonts")
                Wordpress=searchDictionaryKeyValuePartialMatch(eachSiteOutputDict,"Wordpress")
                WordpressVIP=searchDictionaryKeyValuePartialMatch(eachSiteOutputDict,"VIP")
                blocks=searchDictionaryKeyValuePartialMatch(eachSiteOutputDict,"check manually")
                
                eachSiteOutputDict['GoogleFonts']=GoogleFonts
                eachSiteOutputDict['Wordpress']=Wordpress
                eachSiteOutputDict['WPVIP']=WordpressVIP
                
                if LiveWebsite:
                    eachSiteOutputDict['LIVE']="Live Website"
                    if "Live" in eachSiteOutputDict['http']:
                        bestProtocolToScrape="http://"+i['URL']
                    if "Live" in eachSiteOutputDict['httpwww']:
                        bestProtocolToScrape="http://www."+i['URL']
                    if "Live" in eachSiteOutputDict['https']:
                        bestProtocolToScrape="https://"+i['URL']
                    if "Live" in eachSiteOutputDict['https']:
                        bestProtocolToScrape="https://www."+i['URL']
                    newState="Deployed"
                elif BlankWebsite:
                    eachSiteOutputDict['LIVE']="Blank Website"
                    newState="Disposed"
                elif RedirectedWebsite:
                    eachSiteOutputDict['LIVE']="Redirected Website"
                    newState="Disposed"
                else:
                    eachSiteOutputDict['LIVE']="Dead Website"
                    newState="End of Life"
                
                if blocks:
                    eachSiteOutputDict['LIVE']="CHECK MANUALLY"
                    
                eachSiteOutputDict['bestProtocol']=bestProtocolToScrape
                eachSiteOutputDict['URL']=i['URL']

                output.append(eachSiteOutputDict)
            except Exception as e:
                print("***** Something went wrong :  ******")
                print(e)
    return output


def run(filename):
    outputFilename=filename.replace(".csv","Output.csv")
    printHeadless("Outputting to : "+outputFilename)
    with open(outputFilename,'w') as csvfile:
        dataOut=parseCSV(readCSV(filename))
        csvOut = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if countryInCSV and not makeCMDBSuggestions:
            csvOut.writerow(['Country','URL','Website Status', 'GoogleFonts', 'Wordpress', 'Wordpress VIP',  'http','https','httpwww','httpswww','bestProtocol'])
        else:
            csvOut.writerow(['URL','Live', 'GoogleFonts', 'Wordpress', 'Wordpress VIP', 'http','https','httpwww','httpswww', 'bestProtocol'])
        for data in dataOut:
            if countryInCSV and not makeCMDBSuggestions:
                csvOut.writerow([data['Country'],data['URL'],data['LIVE'],data['GoogleFonts'], data['Wordpress'], data['WPVIP'], data['http'],data['https'],data['httpwww'],data['httpswww'],data['bestProtocol']])
            else:
                csvOut.writerow([data['URL'],data['LIVE'],data['GoogleFonts'],data['Wordpress'], data['WPVIP'], data['http'],data['https'],data['httpwww'],data['httpswww'],data['bestProtocol']])
    printHeadless("Done. Saved as : "+outputFilename)

if __name__ == '__main__':
    if len(sys.argv)>1:
        print("Input CSV file : "+ str(sys.argv[1]))
        print("TimeOut set to "+str(timeoutseconds))
        run(sys.argv[1])
    else:
        print("Syntax python "+sys.argv[0]+" <CSVNAME>")
        print("Expected data is CSV format with a column labelled URL, and an optional column labelled Country.")
        
        
