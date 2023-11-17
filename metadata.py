import psycopg2
import json
import rich.progress

file_path = "/home/yc/dataset/amazon/meta_Sports_and_Outdoors.json"

print("Reading Data ...")
data = []
with open(file_path, 'r') as f:
    for line in rich.progress.track(f.readlines()):
        data.append(json.loads(line))

print("Reading Done")
print("Number of rows: {}".format(len(data)))

benchmark = len(data[0].keys())
print("[benchmark]: {}".format(benchmark))
for idx, item in rich.progress.track(enumerate(data)):
    if not len(item.keys()) == benchmark:
        print("[False]: row {} len {}".format(idx, len(item.keys())))
