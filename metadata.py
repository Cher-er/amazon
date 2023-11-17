import psycopg2
import json

file_path = "/home/yc/dataset/amazon/Sports_and_Outdoors.json"

print("Reading Data ...")
data = []
with open(file_path, 'r') as f:
    for line in f.readlines():
        data.append(json.loads(line))

print(len(data))
print(data[0].keys())
