import psycopg2
import json
import rich.progress

file_path = "/home/yc/dataset/amazon/meta_Sports_and_Outdoors.json"

print("Reading Data ...")
data = []
with open(file_path, 'r') as f:
    for idx, line in rich.progress.track(enumerate(f.readlines())):
        raw_data = json.loads(line)
        data.append({
            "category": raw_data["category"],
            "description": raw_data["description"],
            "title": raw_data["title"],
            "also_buy": raw_data["also_buy"],
            "brand": raw_data["brand"],
            "feature": raw_data["feature"],
            "rank": raw_data["rank"],
            "also_view": raw_data["also_view"],
            "main_cat": raw_data["main_cat"],
            "price": raw_data["price"],
            "asin": raw_data["asin"],
        })
        if not len(raw_data["description"]) == 1:
            print("[False] row {} len {}".format(idx, len(raw_data["description"])))

print("Reading Done")
print("Number of rows: {}".format(len(data)))
