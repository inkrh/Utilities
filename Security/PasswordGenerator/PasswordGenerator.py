# !/usr/bin/env python

import string
import random
import sys

passwordLength = 16
sourceString = string.printable

def acceptableCharacters(s):
    if type(s) == str:
        return s.replace(' ','').replace('"','').replace("'","").replace('/','').replace('\\','').replace(';','').replace(':','').replace('\n','').strip()
    return ''

def generate(s,p):
    return ''.join(random.SystemRandom().choice(acceptableCharacters(s)) for _ in range(p))


def Run(filename):
    print("Generating password")
    print("Acceptable Characters are " + str(acceptableCharacters(sourceString)))
    p = generate(sourceString,passwordLength)
    print("Password is " + str(p))
    print("Saving as " + str(filename))
    try:
        with open(filename,'w') as o:
            o.write(p)
        print("Done")
    except:
        print("Saving failure")


if len(sys.argv)<=1:
    print("Syntax : PasswordGenerator <filename>")
else:
    Run(sys.argv[1])
