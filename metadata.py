import psycopg2
import json

file_path = "/home/yc/dataset/amazon/Sports_and_Outdoors.json"
print("Reading Data ...")
with open(file_path, 'r') as f:
    data = json.load(f)

print(len(data))
print(data[0].keys())
