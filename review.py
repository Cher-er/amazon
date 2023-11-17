import psycopg2
import json
import rich.progress
from utils import sanitize_string

file_path = "/home/yc/dataset/amazon/Sports_and_Outdoors.json"

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
    DROP TABLE IF EXISTS review;
    """,
    """
    CREATE TABLE review (
      reviewerID VARCHAR(255),
      reviewTime VARCHAR(255),
      overall FLOAT,
      asin VARCHAR(255),
      reviewerName VARCHAR(255),
      reviewText TEXT,
      summary VARCHAR(255),
      unixReviewTime VARCHAR(255)
    );
    """
)
for command in commands:
    cur.execute(command)
conn.commit()
print("Creating Done")

data = []
count = 1
with open(file_path, 'r') as f:
    for line in rich.progress.track(f.readlines(), description="Reading Data ..."):
        print(f"[Line] {count}")
        raw_data = json.loads(line)
        data.append({
            "reviewerID": raw_data["reviewerID"],
            "reviewTime": raw_data["reviewTime"],
            "overall": float(raw_data["overall"]) if raw_data["overall"] else None,
            "asin": raw_data["asin"],
            "reviewerName": raw_data["reviewerName"],
            "reviewText": raw_data["reviewText"],
            "summary": raw_data["summary"] if "summary" in raw_data else "",
            "unixReviewTime": raw_data["unixReviewTime"]
        })
print("Reading Done")
print("Number of rows: {}".format(len(data)))

for item in rich.progress.track(data, description="Inserting Data ..."):
    # Insert into review
    cur.execute(
        """
        INSERT INTO review
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (item["reviewerID"],
              item["reviewTime"],
              item["overall"],
              item["asin"],
              sanitize_string(item["reviewerName"]),
              sanitize_string(item["reviewText"]),
              sanitize_string(item["summary"]),
              item["unixReviewTime"])
    )
conn.commit()
print("Inserting Done")
