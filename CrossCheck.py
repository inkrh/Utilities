import sqlite3
import csv


#plenty of room for improvement here, but these are the basics
#bulk borrowed from https://pysqlite.readthedocs.io/en/latest/sqlite3.html

def compare(csvOut, dbase1, dbase2, command):
    if type(dbase1) != str or type(dbase2) != str or type(command) != str:
        print "Input type error"
        return

 
    
    con = sqlite3.connect(dbase1)
    con2 = sqlite3.connect(dbase2)
    
    con.isolation_level = None
    con2.isolation_level = None
    
    cur = con.cursor()
    cur2 = con2.cursor()
    
    if sqlite3.complete_statement(command):
        try:
            command = command.strip()
            cur.execute(command)
            cur2.execute(command)
            resultOne = cur.fetchall()
            resultTwo = cur2.fetchall()
            output = [resultOne,resultTwo,resultOne==resultTwo]
            csvOut.writerow(output)

            
            if resultOne == resultTwo:
                print "Matched"
            else:
                print "Not matched"
                
        except sqlite3.Error, e:
            print "An error occurred:", e.args[0]
            con.close()
            con2.close()
            return
        
    else:
        print "Invalid SQL command"
        
    con.close()
    con2.close()
    return


def iterate(filename, dbase1, dbase2, commandList):
    fileInstance = open(filename, 'wb')
    csvHandler = csv.writer(fileInstance)
    
    if type(commandList) == str:
        #single command compare
        compare(csvHandler, dbase1, dbase2, commandList)
    elif type(commandList) == list:
        #list of commands compare
        for c in commandList:
            compare(csvHandler, dbase1, dbase2, c)

    fileInstance.close()


def iterateUsingTextList(fileout,dbase1,dbase2,commandfile):
    f = open(commandfile,'r')
    for lines in f:
        print lines
        iterate(fileout,dbase1,dbase2,lines)

    f.close()            
           
