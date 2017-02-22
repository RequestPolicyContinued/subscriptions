#!/usr/bin/env python
import sys
import json
import warnings
from pprint import pprint

retcode = 0
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
            retcode = 1
        try:
            assert len(str(subscription_parent_serial)) == 10 and str(subscription_parent_serial).isdigit()
            assert len(str(subscription_child_serial)) == 10 and str(subscription_child_serial).isdigit()
        except AssertionError:
            errormsg = ("ERROR: %s: invalid serial format: %s %s")  % (subscription_filename, subscription_parent_serial, subscription_child_serial)
            print(errormsg)
            retcode = 1
    return retcode

retcode = check_serials()
sys.exit(retcode)