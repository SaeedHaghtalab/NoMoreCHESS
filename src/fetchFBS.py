#!/usr/bin/python3
"""
Fetches ESS FBS from available JSON url
"""
import urllib.request
from os import makedirs
makedirs("json",exist_ok = True)
urllib.request.urlretrieve("https://itip.esss.lu.se/chess/fbs.json", "json/fbs.json")
