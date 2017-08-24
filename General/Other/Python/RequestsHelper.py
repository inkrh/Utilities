import requests
import sys
import codecs

def main(address, headers):
    #TODO: split address for unique filename on each
    f = codecs.open('out.txt','w', encoding='utf-8')
    
    f.write(address + '\n')
    
    if(len(headers) >0):
        f.write("headers sent")
        r = requests.get(address, headers)
        for k,v in headers.iteritems():
            f.write(k + ' : ' + v + '\n')
    else:
        r = requests.get(address)

    f.write('\n')
    
    f.write(r.reason)

    f.write('\n')
    if(not r.ok):
            f.write("failed")
            f.close()
            return
        
    f.write('\n')
    j = False
    for k,v in r.headers.iteritems():
            f.write(k + ' : ' + v + '\n')
            if(v == 'application/json'):
                j = true

    f.write('\n')
    outputString=''
    
    if(j):
            outputString = r.json
    else:
            outputString = r.text

    f.write(outputString)
    
    f.close()
    return


http=''
headers = {}
#TODO wire up methods other than GET
method =''

if __name__ == "__main__":
    for i in sys.argv:
        if(i[0:3] == "htt"):
            http =i
        if(':' in i):
            headers[i.split(':')[0]] = i.split(':')[1]
        if(i[0:3]) == "POS":
            method= "POST"


if(len(method) <=0):
           method = "GET"
           
if(len(http ) > 0):
   main(http, headers)










