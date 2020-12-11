import subprocess
import json
import paho.mqtt.publish as publish
from time import sleep

'''mqtt details'''
hostname = ""
auth={'username': "", 'password': ""}

'''device details loaded in to home assistant'''
device = {"device": {"identifiers": ["ups_auto_mqtt"],"name": "UPS Auto MQTT", "model": "pi2b", "manufacturer": "raspberry"}}

bace_topic = "apc_ups/sensor/{}/state"

def get_stats():
    '''gets data from shell'''
    aps_status = subprocess.check_output("apcaccess status",shell=True)
    data = aps_status.decode().splitlines()
    return data

def convert(data):
    dict = {}
    for i in data:
        key = (i.split(":", 1)[0]).rstrip()
        key = (key.replace(" ", "_"))
        key = ("UPS_{}".format(key))
        value = (i[11:])
        dict[key] = value
    return dict

def setup():
    timestamp= ["UPS_DATE", "UPS_STARTTIME", "UPS_XONBATT", "UPS_XOFFBATT", "UPS_END_APC"]
    autoconfig = []
    for i in dict:
        if i in timestamp:
            config = {"name": i, "unique_id" : i, "state_topic": bace_topic.format(i), "device_class": "timestamp"}
        elif "Percent" in dict[i]:
            if "BCHARGE" in (i):
                config = {"name": i, "unique_id" : i, "state_topic": bace_topic.format(i), "unit_of_measurement": "%", "device_class": "battery"}
            else:
                config = {"name": i, "unique_id" : i, "state_topic": bace_topic.format(i), "unit_of_measurement": "%"}
        elif "Volts" in dict[i]:
            config = {"name": i, "unique_id" : i, "state_topic": bace_topic.format(i), "unit_of_measurement": "volt", "device_class": "voltage"}
        elif "Watts" in dict[i]:
            config = {"name": i, "unique_id" : i, "state_topic": bace_topic.format(i), "unit_of_measurement": "Watts", "device_class": "power"}
        elif "Minutes" in dict[i]:
            config = {"name": i, "unique_id" : i, "state_topic": bace_topic.format(i), "unit_of_measurement": "Minutes"}
        elif "Seconds" in dict[i]:
            config = {"name": i, "unique_id" : i, "state_topic": bace_topic.format(i), "unit_of_measurement": "Seconds"}
            #print (config)
        else:
            config = {"name": i, "unique_id" : i, "state_topic": bace_topic.format(i)}
        autoconfig.append(config)
    sleep(.5)
    return autoconfig

def friendly_name(config):
    for i in config:
        if i["name"] == "UPS_BCHARGE":
            i["name"] = "Battery Charge"
        elif i["name"] == "UPS_LINEV":
            i["name"] = "Mains Voltage"
        elif i["name"] == "UPS_BATTV":
            i["name"] = "Battery Voltage"
        elif i["name"] == "UPS_TIMELEFT":
            i["name"] = "Time Left"
        elif i["name"] == "UPS_LOADPCT":
            i["name"] = "Load"
        elif i["name"] == "UPS_DATE":
            i["name"] = "Last Updated"
    return config

def autoconfig(config):
    for i in config:
        setup = ("homeassistant/sensor/"+i['unique_id']+'/config')
        (i).update(device)
        message = json.dumps(i)
        publish.single (setup, message, hostname=hostname, keepalive=5,retain=True)

data = get_stats()
dict = convert(data)
config = setup()
autoconfig(config)
config = friendly_name(config)
sleep(2)
autoconfig(config)
