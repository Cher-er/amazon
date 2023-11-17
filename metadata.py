import psycopg2
import json
import rich.progress

file_path = "/home/yc/dataset/amazon/meta_Sports_and_Outdoors.json"

pgsql_parameter = {
    "host": "localhost",
    "port": 5433,
    "database": "amazon",
    "user": "postgres",
    "password": "123456",
}

print("Connecting PostgreSQL ...")
conn = psycopg2.connect(host=pgsql_parameter["host"],
                        port=pgsql_parameter["port"],
                        database=pgsql_parameter["database"],
                        user=pgsql_parameter["user"],
                        password=pgsql_parameter["password"])
print("Connecting Done")

print("Reading Data ...")
data = []
with open(file_path, 'r') as f:
    for idx, line in rich.progress.track(enumerate(f.readlines())):
        raw_data = json.loads(line)
        print("[Price] {}".format(raw_data["price"]))
        raw_data["price"] = float(raw_data["price"][1:]) if raw_data["price"][1:] else None
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

print("Reading Done")
print("Number of rows: {}".format(len(data)))

commands = (
    """
    CREATE TABLE metadata (
      asin varchar(255),
      title varchar(255),
      brand varchar(255),
      rank varchar(255),
      main_car varchar(255),
      price integer
    );
    """
)
