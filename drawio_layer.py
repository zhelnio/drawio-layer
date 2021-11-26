#!/usr/bin/env python3

# Copyright (c) 2020, Stanislav Zhelnio
# SPDX-License-Identifier: MIT

"""
Layer management script for github.com/jgraph/drawio
Allows to list/show/hide layers on diagram page
Tested with draw.io 13.6.2
"""

import argparse
from os import error
import sys
import xml.etree.ElementTree as ET
from tabulate import tabulate
import warnings

actions = [
    "idle",
    "show",
    "hide",
    "show_only",
    "hide_only",
]

def main():
    args = parse_args()
    # check_file(args.file)
    tree = ET.parse(args.file)

    check_tree(tree)

    # search for layers
    nodes = find_layers(tree, args.page_index)

    # apply changes
    if args.action_type == "show":
        force_visibility (nodes, True, apply_list=args.name)
    if args.action_type == "hide":
        force_visibility (nodes, False, apply_list=args.name)
    if args.action_type == "show_only":
        force_visibility (nodes, False, except_list=args.name)
    if args.action_type == "hide_only":
        force_visibility (nodes, True, except_list=args.name)

    # print layers list
    info = layers_filter(nodes, list_visible=args.list_visible or args.list, \
                                list_hidden=args.list_hidden or args.list )
    layers_print(info, args.verbose)

    # save changes
    if args.action_type != "idle":
        tree.write(args.file)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Layer management script for github.com/jgraph/drawio",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("file", type=str, help="file name")
    parser.add_argument("-l", "--list",    action='store_true', help="list layers")
    parser.add_argument("-lv", "--list-visible", action='store_true', help="list visible layers")
    parser.add_argument("-lh", "--list-hidden", action='store_true', help="list hidden layers")
    parser.add_argument("-V", "--verbose", action='store_true', help="verbose mode")
    parser.add_argument("-p", "--page-index", type=int, default=0, help="selects a specific page")
    parser.add_argument("-n", "--name", type=str, nargs='+', help="layer names", default=[])
    parser.add_argument("-t", "--action-type", choices=actions, default="idle",
                        help="Action Type. Allowed values are: " + ", ".join(actions))

    args = parser.parse_args()
    return args

def check_tree(tree):
    msg = """This script works with uncompressed draw.io files: You can set it in drawio GUI: File -> Properties"""

    compressed = False
    try:
        root = tree.getroot()
        compressed = root.attrib['compressed']!="false"
    except:
        compressed = True

    if(compressed):
        sys.exit(msg)

def find_layers(tree, page_index):
    try:
        root = tree.getroot()
        page = root.findall(".//diagram/mxGraphModel/root")
        page_id = page[page_index].find('mxCell').attrib['id']
        query = ".//mxCell[@parent='%s']" % page_id
        return root.findall(query)
    except:
        msg = "No layers found. Please check input args."
        sys.exit(msg)

def get_layer_name(node) -> str:
    return node.get("value", "Background")

def get_layer_visibility(node) -> bool:
    return node.get("visible", '1') == '1'

def set_layer_visibility(node, visible=True):
    node.attrib['visible'] = '1' if visible else '0'

def layers_filter(nodes=[], list_visible=True, list_hidden=True):
    data = []

    for node in nodes:
        layer_name = get_layer_name(node)
        layer_visible = get_layer_visibility(node)

        if (list_visible and layer_visible) or \
        (list_hidden  and not layer_visible):
            data.append([layer_name, layer_visible])
    return data

def layers_print(data, verbose=False):
    if verbose:
        print(tabulate(data, tablefmt="plain"))
    else:
        for item in data:
            print(item[0])

def force_visibility(nodes=[], visible:bool=False, except_list=[], apply_list=[]):
    for node in nodes:
        layer_name = get_layer_name(node)

        if layer_name in apply_list and layer_name in except_list:
            warnings.warn("%s is both in apply and except lists!")

        elif len(apply_list) > 0 and layer_name in apply_list:
            set_layer_visibility(node, visible)
        
        elif len(except_list) > 0:
            set_layer_visibility(node, visible != (layer_name in except_list))

if __name__ == '__main__':
    main()
