### code for grabbing forecast.io prediction snapshots

import urllib
import json
import time
import csv
import os

root = os.getcwd()

base_url = "https://api.forecast.io/forecast/"
api_key = open(root + "/api_keys/forecast_api_key").read()
options = "?exlude=flags,alerts,minutely"

now = time.strftime("%Y-%m-%d_%H:%M")

out_json = root + "/forecast_" + now + ".json"
con_json = open(out_json, "w")
out_csv = open(root + "/forecast_" + now + ".csv", "w")
con_csv = csv.writer(out_csv)

# st. paul coordinates, per google
lat = "44.9442"
lon = "-93.0936"

url = base_url + api_key + "/" + lat + "," + lon + options

data = urllib.urlopen(url).read()
data_js = json.loads(data)

fields = [ "precipAccumulation",
           "precipType",
           "cloudCover",
           "humidity",
           "visibility",
           "summary",
           "pressure",
           "windSpeed",
           "temperature",
           "time",
           "windBearing",
           "precipIntensity",
           "dewPoint",
           "precipProbability",
           "temperatureMin",
           "temperatureMax"
]

the_data = {}

for item in data_js["hourly"]["data"] :
    snap_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(item["time"])))
    snapshot = {}
    for key, value in item.items() :
        if key in fields :
            snapshot[key] = str(value)

    snapshot["type"] = "hourly"
    snapshot["src"] = "forecast.io"
    the_data[snap_time] = snapshot

for item in data_js["daily"]["data"] :
    snap_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(item["time"])))
    snapshot = {}
    for key, value in item.items() :
        if key in fields :
            snapshot[key] = str(value)
    
    snapshot["type"] = "daily"
    snapshot["src"] = "forecast.io"
    the_data[snap_time] = snapshot

crnt = data_js["currently"]
snapshot = {}
for key in crnt.keys() :
    snap_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(crnt["time"])))
    if key in fields :
        snapshot[key] = crnt[key]

    snapshot["type"] = "current"
    snapshot["src"] = "forecast.io"
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
    
json.dump(the_data, con_json, indent = 4)
con_json.close()
out_csv.close()

print "done"
