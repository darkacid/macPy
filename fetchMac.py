#!/usr/bin/env python3


import mactable
import csv



hostFile = csv.reader(open('hostbase.csv', newline=''), delimiter=';', quotechar='|')


for switch in hostFile:
    if not switch:
        continue
    mactable.HOST     = switch[0]
    mactable.username = switch[1]
    mactable.password = switch[2]
    print (switch[0],switch[1],switch[2])
    macTable = mactable.getMacTable()
    print ("Host:",switch[0],macTable)

