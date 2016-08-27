### code for grabbing wunderground prediction snapshots

import urllib
import json
import time
import csv
import os

root = os.getcwd()

base_url = "http://api.wunderground.com/api/"
api_key = open(root + "/api_keys/wunder_api_key").read()

now = time.strftime("%Y-%m-%d_%H:%M")

out_json = root + "/wunder_" + now + ".json"
con_json = open(out_json, "w")
out_csv = open(root + "/wunder_" + now + ".csv", "w")
con_csv = csv.writer(out_csv)

# st. paul coordinates, per google
lat = "44.9442"
lon = "-93.0936"

url = base_url + api_key + "/hourly/q/" + lat + "," + lon + ".json"

data = urllib.urlopen(url).read()
data_js = json.loads(data)

fields = { "mslp" : "metric" ,
           "temp" : "english",
           "dewpoint" : "metric",
            "wdir" : "degrees",
            "qpf" : "metric",
            "humidity" : 0,
            "sky" : 0,
            "snow" : "metric",
            "pop" : 0,
            "wspd" : "metric",
            "condition" : 0
}

the_data = {}

for item in data_js["hourly_forecast"] :
    snap_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(item["FCTTIME"]["epoch"])))
    snapshot = {}
    for key, value in item.items() :
        if key in fields :
            if fields[key] == 0 : snapshot[key] = str(value)
            else :  snapshot[key] = str(value[fields[key]])
	    snapshot["type"] = "hourly"
	    snapshot["src"] = "wunder"
    the_data[snap_time] = snapshot

# for item in data_js["daily"]["data"] :
#     snap_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(item["time"])))
#     snapshot = {}
#     for key, value in item.items() :
#         if key in fields :
#             snapshot[key] = str(value)
# 	    snapshot["type"] = "daily"
# 	    snapshot["src"] = "forecast.io"
#     the_data[snap_time] = snapshot

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
