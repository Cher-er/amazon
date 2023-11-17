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
cur = conn.cursor()
print("Connecting Done")

print("Creating Tables ...")
commands = (
    """
    DROP TABLE IF EXISTS TABLE metadata;
    """,
    """
    CREATE TABLE metadata (
      asin VARCHAR(255),
      title VARCHAR(255),
      brand VARCHAR(255),
      rank VARCHAR(255),
      main_cat VARCHAR(255),
      price FLOAT
    );
    """,
    """
    DROP TABLE IF EXISTS TABLE category;
    """,
    """
    CREATE TABLE category (
      cate_id INTEGER,
      category VARCHAR(255)
    );
    """,
    """
    DROP TABLE IF EXISTS TABLE meta_cate;
    """,
    """
    CREATE TABLE meta_cate (
      asin VARCHAR(255),
      cate_id INTEGER
    );
    """,
    """
    DROP TABLE IF EXISTS TABLE description;
    """,
    """
    CREATE TABLE description (
      asin VARCHAR(255),
      description VARCHAR(255)
    );
    """,
    """
    DROP TABLE IF EXISTS TABLE also_buy;
    """,
    """
    CREATE TABLE also_buy (
      asin VARCHAR(255),
      buy_asin VARCHAR(255)
    );
    """,
    """
    DROP TABLE IF EXISTS TABLE also_view;
    """,
    """
    CREATE TABLE also_view (
      asin VARCHAR(255),
      view_asin VARCHAR(255)
    );
    """,
    """
    DROP TABLE IF EXISTS TABLE feature;
    """,
    """
    CREATE TABLE feature (
      asin VARCHAR(255),
      feature VARCHAR(255)
    );
    """
)
for command in commands:
    cur.execute(command)
cur.commit()
print("Creating Done")

print("Reading Data ...")
data = []
with open(file_path, 'r') as f:
    for line in rich.progress.track(f.readlines()):
        raw_data = json.loads(line)
        raw_data["price"] = float(raw_data["price"][1:]) if raw_data["price"][1:].isdigit() else None
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

print("Inserting Data ...")
for item in rich.progress.track(data):
    cur.execute(
        """
        INSERT INTO metadata
        VALUES ({}, {}, {}, {}, {}, {});
        """.format(item["asin"], item["title"], item["brand"], item["rank"], item["main_cat"], item["price"])
    )
cur.commit()
print("Inserting Done")
