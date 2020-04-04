import csv, json
csvFilePath = 'metronames.csv'
jsonFilePath = 'metronames.json'

import csv
import json

csvfile = open(csvFilePath, 'r', encoding='UTF-8')  #encoding='UTF-8'
jsonfile = open(jsonFilePath, 'w')

fieldnames = ("name","place","city")
reader = csv.DictReader(csvfile, fieldnames, delimiter=';')
for row in reader:
    json.dump(row, jsonfile, ensure_ascii=False)
    jsonfile.write('\n')