#!/usr/bin/env python
import sys
import os
import glob
import json
from pprint import pprint

subscription_list_filename = ('official.json')
subscription_list_file = open(subscription_list_filename)
data = json.load(subscription_list_file)

def check_serials():
    subscriptions = data["subscriptions"]
    for i in subscriptions.keys():
        subscription_parent_serial = subscriptions[i]["serial"]
        subscription_filename = str('official-' + i + '.json')
        subscription_file = open(subscription_filename)
        subscription_data = json.load(subscription_file)
        subscription_child_serial = subscription_data["metadata"]["serial"]
        try:
            assert subscription_parent_serial == subscription_child_serial
        except AssertionError:
            errormsg = ("ERROR: serials do not match in %s : %s %s") % (subscription_filename, subscription_parent_serial, subscription_child_serial)
            print(errormsg)
        try:
            assert len(str(subscription_parent_serial)) == 10 and str(subscription_parent_serial).isdigit()
            assert len(str(subscription_child_serial)) == 10 and str(subscription_child_serial).isdigit()
        except AssertionError:
            errormsg = ("ERROR: %s: invalid serial format: %s %s")  % (subscription_filename, subscription_parent_serial, subscription_child_serial)
            print(errormsg)

def check_blank_lines(): #PAS MARCHE
    for filename in glob.glob("*.json"):
        jsonfile = open(filename)
        for line in jsonfile.read().split(os.linesep):
            assert line.strip() != ""

check_serials()
check_blank_lines()