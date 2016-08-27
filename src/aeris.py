### code for grabbing aeris prediction snapshots
# need to run this just before the hour, as it appears to only
# grab from the next hour, even with the from= option
# it was 14:08 and I tried to get from 14:00 on and it still
# starts at 15:00

import urllib
import json
import time
import csv
import os

root = os.getcwd()

base_url = "http://api.aerisapi.com/forecasts/closest"
api_id = open(root + "/api_keys/aeris_api_id").read()
api_secret = open(root + "/api_keys/aeris_api_secret").read()

now = time.strftime("%Y-%m-%d_%H:%M")

out_json = root + "/aeris_" + now + ".json"
con_json = open(out_json, "w")
out_csv = open(root + "/aeris_" + now + ".csv", "w")
con_csv = csv.writer(out_csv)

print out_json

# st. paul coordinates, per google
lat = "44.9442"
lon = "-93.0936"

fields = [
    "dewpointC",
    "pop",
    "tempC",
    "tempF",
    "maxTempC",
    "minTempC",
    "humidity",
    "weather",
    "weatherPrimary",
    "snowCM",
    "windSpeedKPH",
    "precipMM",
    "windDirDEG",    
    "sky",
    "pressureMB",    
    "iceaccum",
    "timestamp"
]

url = base_url + "?" + "p=" + lat + "," + lon + "&" + \
      "filter=1hr&" + "limit=49&" + \
      "client_id=" + api_id + "&" + "client_secret=" + api_secret

data = urllib.urlopen(url).read()
data_js = json.loads(data)

the_data = {}

for item in data_js["response"][0]["periods"] :
    snap_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(item["timestamp"])))
    snapshot = {}
    for key, value in item.items() :
        if key in fields :
            snapshot[key] = str(value)
    snapshot["type"] = "hourly"
    snapshot["src"] = "aeris"
    the_data[snap_time] = snapshot

header = list(fields)
header.insert(0, "key")
header.insert(0, "type")
header.insert(0, "src")
con_csv.writerow(header)

for key in the_data.keys() :
    temp = the_data[key]
    string = list()
    string.append(temp["src"])
    string.append(temp["type"])
    string.append(str(key))
    
    for field in fields :
        string.append(temp.get(field, "NA"))
    con_csv.writerow(string)


url = base_url + "?" + "p=" + lat + "," + lon + "&" + \
      "filter=day&" + "limit=10&" + \
      "client_id=" + api_id + "&" + "client_secret=" + api_secret

data = urllib.urlopen(url).read()
data_js = json.loads(data)

the_data = {}

for item in data_js["response"][0]["periods"] :
    snap_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(item["timestamp"])))
    snapshot = {}
    for key, value in item.items() :
        if key in fields :
            snapshot[key] = str(value)
    snapshot["type"] = "daily"
    snapshot["src"] = "aeris"
    the_data[snap_time] = snapshot

for key in the_data.keys() :
    temp = the_data[key]
    string = list()
    string.append(temp["src"])
    string.append(temp["type"])
    string.append(str(key))
    
    for field in fields :
        string.append(temp.get(field, "NA"))
    con_csv.writerow(string)
    
json.dump(the_data, con_json, indent = 4)
con_json.close()
out_csv.close()

print "done"
