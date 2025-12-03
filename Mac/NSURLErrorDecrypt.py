#!/usr/bin/python

import string
import sys

def TranslateCode(code):
    if("998" in str(code)):
        return "Unknown error"
    if("999" in str(code)):
        return "Cancelled"
    if("1000" in str(code)):
        return "Bad URL"

    if("1001" in str(code)):
        return "Timed out"

    if("1002" in str(code)):
        return "Unsupported URL"

    if("1003" in str(code)):
        return "Cannot find host"

    if("1004" in str(code)):
        return "Cannot connect to host"

    if("1005" in str(code)):
        return "Network connection lost"

    if("1006" in str(code)):
        return "DNS lookup failed"

    if("1007" in str(code)):
        return "Too many redirects"

    if("1008" in str(code)):
        return "Resource unavailable"

    if("1009" in str(code)):
        return "Not connected to the internet"

    if("1010" in str(code)):
        return "Redirect to a non-existant location"

    if("1011" in str(code)):
        return "Bad response from server"

    if("1012" in str(code)):
        return "User cancelled the authentication"

    if("1013" in str(code)):
        return "User authentication required"

    if("1014" in str(code)):
        return "Zero byte resource"

    if("1015" in str(code)):
        return "Cannot decode the raw data"

    if("1016" in str(code)):
        return "Cannot decode the content data"

    if("1017" in str(code)):
        return "Cannot parse the response"

    if("1018" in str(code)):
        return "International roaming is off"

    if("1019" in str(code)):
        return "A call is in progress"

    if("1020" in str(code)):
        return "Data is not allowed"

    if("1021" in str(code)):
        return "Request body stream is exhausted"

    if("1100" in str(code)):
        return "File does not exist"

    if("1101" in str(code)):
        return "File is a directory"

    if("1102" in str(code)):
        return "No permissions to read the file"

    if("1103" in str(code)):
        return "Data length exceeds the maximum"

    return "No information available"




if __name__ == '__main__':
    try:
        for i in sys.argv:
            print(i + "\t" + TranslateCode(i)+"\n")

    except:
        print("Error. Invalid arguments?\n")

