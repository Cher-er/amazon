import psycopg2
import json
import rich.progress

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
      reviewName VARCHAR(255),
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
with open(file_path, 'r') as f:
    for line in rich.progress.track(f.readlines(), description="Reading Data ..."):
        raw_data = json.loads(line)
        data.append({
            "reviewerID": raw_data["reviewerID"],
            "reviewTime": raw_data["reviewTime"],
            "overall": float(raw_data["overall"]) if raw_data["overall"] else None,
            "asin": raw_data["asin"],
            "reviewName": raw_data["reviewName"],
            "reviewText": raw_data["reviewText"],
            "summary": raw_data["summary"],
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
        """, (item["reviewerID"], item["reviewTime"], item["overall"], item["asin"],
              item["reviewName"], item["reviewText"], item["summary"], item["unixReviewTime"])
    )
conn.commit()
print("Inserting Done")
