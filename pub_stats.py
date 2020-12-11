import subprocess
import json
import paho.mqtt.publish as publish
import argparse

'''mqtt details'''
hostname = ""
auth={'username': "", 'password': ""}

'''device details loaded in to home assistant'''
device = {"device": {"identifiers": ["ups_auto_mqtt"],"name": "UPS Auto MQTT", "model": "pi2b", "manufacturer": "raspberry"}}

float_keys_list = ["UPS_ALARMDEL", "UPS_BATTV",	"UPS_BCHARGE", "UPS_CUMONBATT", "UPS_HITRANS", "UPS_LINEV", "UPS_LOADPCT", "UPS_LOTRANS", "UPS_MAXTIME", "UPS_MBATTCHG", "UPS_MINTIMEL", "UPS_NOMBATTV", "UPS_NOMINV", "UPS_NOMPOWER", "UPS_TIMELEFT", "UPS_TONBATT",]

def get_stats():
    '''gets data from shell'''
    aps_status = subprocess.check_output("apcaccess status", shell=True)
    data = aps_status.decode().splitlines()
    return data

def convert(data):
    '''converts data in to dictionary '''
    dict = {}
    for i in data:
        key = (i.split(":", 1)[0]).rstrip()
        key = (key.replace(" ", "_"))
        key = ("UPS_{}".format(key))
        value = (i[11:])
        dict[key] = value
    return dict

def autopub():
    for i in dict:
        topic = ("apc_ups/sensor/{}/state".format(i))
        if i in float_keys_list:
            value = (dict[i].split(" ", 1)[0])
            message = int(float(value))
        else:
            message = (dict[i])
        publish.single (topic, message, hostname=hostname, keepalive=5,retain=True)

if __name__ == '__main__':
    data = get_stats()
    dict = convert(data)
    autopub()
