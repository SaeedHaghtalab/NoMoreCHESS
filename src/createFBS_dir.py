#!/usr/bin/python3

import json
import os
import sys
from anytree import Node, RenderTree, ContRoundStyle
import argparse

parser = argparse.ArgumentParser(description='Create folder structure based on FBS')
parser.add_argument("fbsInput", help="Path to JSON file containing the pre-filtered FBS nodes")
parser.add_argument("-p", "--print", action="store_true",help="Only prints the FBS tree")
args = parser.parse_args()

fbsInput = args.fbsInput

fPath = os.path.dirname(os.path.realpath(__file__))
def dir(n, cwd = fPath):
    cwd = cwd + "/" + n.name + " [" + (n.desc).replace(os.sep,'\\') + "]"
    if n.is_leaf:
        with open(cwd, 'w'): pass
        return
    os.makedirs(cwd)
    for child in n.children:
        dir(child, cwd)

with open(fPath + '/' + fbsInput) as inFile:
    jfbs=json.load(inFile)

root = Node("=ESS", Desc = "ESS")

for jnode in jfbs:
    fullTag = jnode['tag']

    tnode = root
    for part in fullTag.split(".")[1:]:
        child = next((c for c in tnode.children if c.name == part), None)
        if child is None:
            child = Node(part, parent=tnode, Desc = jnode['description'])
        tnode = child
if args.print:
    print(RenderTree(root, style=ContRoundStyle()))
else:
    dir(root)
