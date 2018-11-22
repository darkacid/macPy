#!/usr/bin/env python3
'''
Python script for retreiving mac table by telnet.
Usage: run as such: ./mactable.py host username password.
Can return list containing items in this format: [vlanID, mac address, port]
'''
import telnetlib
import time
import sys
import re

if __name__ =="__main__":
    if len(sys.argv) < 4:
        print("launch with:  ",sys.argv[0],'host','username','password')
        exit(1)
    
    HOST = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
try :
    HOST
    username
    password
except: 
    raise ValueError("Host, username or password undefined")

def TelnetGet(HOST,username,password,command):

    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"login: ")
    tn.write(str.encode(username)+b"\n")

    tn.read_until(b"Password: ")
    tn.write(str.encode(password)+b"\n")

    authStrReturn = tn.read_until(b">",timeout=1) 
    #Continue if correct credentials
    if "Incorrect" in authStrReturn.decode():
        raise ValueError("Credentials incorrect for: ",HOST)
    tn.write(str.encode(command)+b"\n")

    sw_output_normalized = []

    #Read data from switch after "debug info, periodically hitting 'enter',
    #filling sw_output_normalized in the process.
    while True:

        response = tn.read_until(b"--More",timeout=1)
        response = response.decode()
        responseList = response.split('\n')
        for item in responseList:
            if item == "\r\x1b[K\r--More":
                continue
            #print(item)
            sw_output_normalized.append(item)
        tn.write(str.encode("\n"))
        if "Total" in response:
            break
    tn.close()
    return sw_output_normalized

def parseCLIOutput(sw_output_normalized):
    '''
    Create macTable from full command output "debug info"
    
    777      ff:ff:ff:ff:ff:ff   Learnt   Gi0/24
    '''
    pattern ="([0-9]{1,4})[\ A-Za-z]+([a-zA-Z\:0-9]{17})[\ A-Za-z]+([A-Za-z]{2}[0-9]{1,2}/[0-9]{1,2})"
    macTable = [] #List of lists containing items in this format: [vlanID,mac address, port]
    #777 ff:ff:ff:ff:ff:ff Gi0/24
    for item in sw_output_normalized:
        if "Learnt" in item:
            found = re.search(pattern,item)
            if found:
                
                vlanid = found.group(1)
                macAddr = found.group(2)
                port = found.group(3)
                
                macTable.append([vlanid,macAddr,port])
            else:
                raise ValueError("Regex match failed: " + item )
    macTable.append(len(macTable)) #Append length of the actual mac table to the list.
    return macTable

sw_output_normalized = TelnetGet(HOST,username,password,"debug info")
macTable = parseCLIOutput(sw_output_normalized)
print(macTable)

