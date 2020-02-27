#!/usr/bin/python3

import json
import os
import sys
from anytree import Node, RenderTree, ContRoundStyle
import argparse

parser = argparse.ArgumentParser(description='Create folder structure based on FBS')
parser.add_argument("fbsInput",             help="JSON file containing the FBS nodes")
parser.add_argument("-f","--filter",        help="FBS prefix to filter nodes on", nargs='?', default="=ESS")
parser.add_argument("-p",   "--print",      help="Only prints the FBS tree", action="store_true")
parser.add_argument("-d",   "--dir",        help="Path to where direcotry structure be created.", nargs='?', default='', const=".", type=str )
parser.add_argument("-r",   "--recursive",  help="Present Nodes recuresively i.e. =ESS.ACC.E02 rather than E02", action="store_true")
parser.add_argument("-s",   "--sep",        help="Node Seperator", default='.')
parser.add_argument(        "--desc",       help="Add description to tree output", action="store_true")
parser.add_argument('-l',   "--lim",        help="limit folder name to 248", action="store_true")

args = parser.parse_args()

fbsInput = args.fbsInput
fnode = args.filter.strip()
if fnode[0] != '=':
    fnode = "="+ fnode
dirpath = str(args.dir).strip()

sep = args.sep
fnode.replace('.', sep)

## Create directory structure
def dir(n, cwd):
    if args.recursive:
        dirname = n.strpath + n.name
    else:
        dirname = n.name
    if args.desc:
        dirname = dirname + " [" + n.desc + "]"

    if args.lim:
        dirname = dirname[:248]
    cwd = cwd + "/" + dirname

    if n.is_leaf:
        with open(cwd, 'w'): pass
        return
    os.makedirs(cwd)
    for child in n.children:
        dir(child, cwd)

with open(fbsInput) as inFile:
    jfbs=json.load(inFile)

# Recursive node path generator
def strpathGen(node, npath=''):
    if node.is_root:
        return npath
    npath = node.parent.name + sep + npath
    return strpathGen(node.parent, npath)

root = Node(fnode, separator = sep, strpath = '')

# Fill tree nodes from json
for jnode in jfbs:
    fullTag = jnode['tag']
    if fullTag.startswith(fnode):
        if fullTag == fnode and not hasattr('root', 'desc'):
            root.desc=jnode['description']
        fullTag = fullTag.replace(fnode,'')
        tnode = root
        for part in fullTag.split("."):
            if part:
                child = next((c for c in tnode.children if c.name == part), None)
                if child is None:
                    child = Node(part, parent=tnode, desc = jnode['description'], separator = sep)
                    child.desc = child.desc.replace("\n",'')
                    child.desc = child.desc.replace(os.sep,'\\')
                    child.strpath = strpathGen(child)
                tnode = child
if args.print:
    for pre, _, node in RenderTree(root, style=ContRoundStyle()):
        desc=''
        strpath=''
        if args.recursive:  strpath = node.strpath
        if args.desc:
            print("%s%s (%s)" % (pre, strpath + node.name, node.desc))
        else:
            print("%s%s" % (pre, strpath + node.name))

if dirpath:
    dir(root, dirpath)
