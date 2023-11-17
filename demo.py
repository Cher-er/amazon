import psycopg2
import json
import rich.progress
from utils import sanitize_string, isfloat

file_path = "/home/yc/dataset/amazon/meta_Sports_and_Outdoors.json"

data = []
with open(file_path, 'r') as f:
    blank_count = 0
    range_count = 0
    for line in rich.progress.track(f.readlines(), description="Reading Data ..."):
        raw_data = json.loads(line)
        data.append({
            "category": raw_data["category"],
            "description": raw_data["description"],
            "title": raw_data["title"],
            "also_buy": raw_data["also_buy"],
            "brand": raw_data["brand"],
            "feature": raw_data["feature"],
            "rank": raw_data["rank"] if isinstance(raw_data["rank"], list) else [raw_data["rank"]],
            "also_view": raw_data["also_view"],
            "main_cat": raw_data["main_cat"],
            "price": float(raw_data["price"][1:]) if isfloat(raw_data["price"][1:]) else None,
            "asin": raw_data["asin"]
        })
        if not isfloat(raw_data["price"][1:]):
            if not raw_data["price"]:
                blank_count += 1
            if '-' in raw_data["price"]:
                range_count += 1
print("Reading Done")
print("Number of rows: {}".format(len(data)))
print(f"Blank {blank_count} Range {range_count}")
