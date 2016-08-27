### code for grabbing openweathermap prediction snapshots

import urllib
import json
import time
import csv

base_url = "http://openweathermap.org/data/2.5/forecast"
api_key = "b954d932fb73b317916f5f576ebf91e5"

now = time.strftime("%Y-%m-%d_%H:%M")

root = "/home/jwhendy/vault/personal/weather-pred/"
out_json = root + "owmap_" + now + ".json"
con_json = open(out_json, "w")
out_csv = open(root + "owmap_" + now + ".csv", "w")
con_csv = csv.writer(out_csv)

# st. paul coordinates, per google
lat = "44.9442"
lon = "-93.0936"

url = base_url + "?" + "lat=" + lat + "&lon=" + lon + "&units=metric" + "&appid=" + api_key

data = urllib.urlopen(url).read()
data_js = json.loads(data)

fields = {
    "main" : [ "temp", "pressure", "humidity" ],
#    "weather" : [ "description" ],
    "wind" : [ "speed", "deg" ],
    "rain" : [ "3h" ],
    "snow" : [ "3h" ],
    "clouds" : [ "all" ]
}

the_data = {}

for item in data_js["list"] :
    snap_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(item["dt"])))
    snapshot = {}
    for key in fields.keys() :
        if key in item.keys() :
             for x in fields[key] :
                 if x in item[key] :
                     snapshot[key + "_" + x] = item[key][x]
                     
    snapshot["desc"] = item["weather"][0]["description"]
    snapshot["type"] = "hourly"
    snapshot["src"] = "owmap"
    
    the_data[snap_time] = snapshot

header = list()
for key in fields.keys() :
    for val in fields[key] :
        header.append(key + "_" + val)

header.insert(0, "desc")
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
    string.append(temp["desc"])
    
    for key in fields.keys() :
        for val in fields[key] :
            string.append(temp.get(key + "_" + val, "NA"))
    con_csv.writerow(string)
    
json.dump(the_data, con_json, indent = 4)

con_json.close()
out_csv.close()

print "done"
