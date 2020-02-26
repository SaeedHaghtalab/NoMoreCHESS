#!/usr/bin/python3
import json
import urllib.request
import time
with open("json/fbs.json") as fbsNodes:
    listFBS = json.load(fbsNodes)
    with open("json/all.conf","w+") as outfile:
        for node in listFBS:
            if "ESS.ACC.A01" in node['tag']:
                outfile.write(node['tag'] + " " + node['description'] + "\n")
