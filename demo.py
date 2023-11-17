import json
import rich.progress

file_path = "/home/yc/dataset/amazon/meta_Sports_and_Outdoors.json"

data = []
with open(file_path, 'r') as f:
    for idx, line in rich.progress.track(enumerate(f.readlines()), description="Reading Data ..."):
        raw_data = json.loads(line)
        print(raw_data["price"], raw_data["price"][1:], raw_data["price"][1:].isdigit())
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
            "price": float(raw_data["price"][1:]) if raw_data["price"][1:].isdigit() else None,
            "asin": raw_data["asin"],
        })

print("Reading Done")
print("Number of rows: {}".format(len(data)))
