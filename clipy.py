#!/usr/bin/env python3

import telnetlib
import time
import sys
if __name__ =="__main__":
    HOST = sys.argv[1]
try :
    HOST
except: 
    raise ValueError("Host undefined")


username = "admin"
password = "admin"


tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(str.encode(username)+b"\n")

tn.read_until(b"Password: ")
tn.write(str.encode(password)+b"\n")

tn.read_until(b">")

tn.write(str.encode("debug info")+b"\n")
while True:

    response = tn.read_until(b"--More",timeout=1)
    response = response.decode()
    responseList = response.split('\n')
    for item in responseList:
        if item == "\r\x1b[K\r--More":
            responseList.remove(item)
            continue
        print(item)
    tn.write(str.encode("\r \n"))
    if "Total" in response:
        break
tn.close()

