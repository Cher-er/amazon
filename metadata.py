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
    DROP TABLE IF EXISTS metadata;
    """,
    """
    CREATE TABLE metadata (
      asin VARCHAR(255),
      title TEXT,
      brand TEXT,
      rank TEXT,
      main_cat TEXT,
      price FLOAT
    );
    """,
    """
    DROP TABLE IF EXISTS category;
    """,
    """
    CREATE TABLE category (
      cate_id INTEGER,
      category TEXT
    );
    """,
    """
    DROP TABLE IF EXISTS meta_cate;
    """,
    """
    CREATE TABLE meta_cate (
      asin VARCHAR(255),
      cate_id INTEGER
    );
    """,
    """
    DROP TABLE IF EXISTS also_buy;
    """,
    """
    CREATE TABLE also_buy (
      asin VARCHAR(255),
      buy_asin VARCHAR(255)
    );
    """,
    """
    DROP TABLE IF EXISTS also_view;
    """,
    """
    CREATE TABLE also_view (
      asin VARCHAR(255),
      view_asin VARCHAR(255)
    );
    """,
    """
    DROP TABLE IF EXISTS feature;
    """,
    """
    CREATE TABLE feature (
      asin VARCHAR(255),
      feature TEXT
    );
    """,
    """
    DROP TABLE IF EXISTS description;
    """,
    """
    CREATE TABLE description (
      asin VARCHAR(255),
      description TEXT
    );
    """
)
for command in commands:
    cur.execute(command)
conn.commit()
print("Creating Done")

data = []
limit, count = 10000, 0
with open(file_path, 'r') as f:
    for line in rich.progress.track(f.readlines(), description="Reading Data ..."):
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
            "main_cat": repr(raw_data["main_cat"]),
            "price": raw_data["price"],
            "asin": raw_data["asin"],
        })
        count += 1
        if count >= limit:
            break

print("Reading Done")
print("Number of rows: {}".format(len(data)))

categories = []
for item in rich.progress.track(data, description="Inserting Data ..."):
    # Insert into metadata
    cur.execute(
        """
        INSERT INTO metadata
        VALUES (%s, %s, %s, %s, %s, %s);
        """, (item["asin"], item["title"], item["brand"], item["rank"], item["main_cat"], item["price"])
    )
    # Insert into also_buy
    for buy_asin in item["also_buy"]:
        cur.execute(
            """
            INSERT INTO also_buy
            VALUES (%s, %s)
            """, (item["asin"], buy_asin)
        )
    # Insert into also_view
    for view_asin in item["also_view"]:
        cur.execute(
            """
            INSERT INTO also_view
            VALUES (%s, %s)
            """, (item["asin"], view_asin)
        )
    # Insert into category and meta_cate
    for category in item["category"]:
        if category not in categories:
            cur.execute(
                """
                INSERT INTO category
                VALUES (%s, %s)
                """, (len(category) + 1, category)
            )
            categories.append(category)
        cur.execute(
            """
            INSERT INTO meta_cate
            VALUES (%s, %s)
            """, (item["asin"], categories.index(category) + 1)
        )
    # Insert into feature
    for feature in item["feature"]:
        cur.execute(
            """
            INSERT INTO feature
            VALUES (%s, %s)
            """, (item["asin"], feature)
        )
    # Insert into description
    for description in item["description"]:
        cur.execute(
            """
            INSERT INTO description
            VALUES (%s, %s)
            """, (item["asin"], description)
        )
conn.commit()
print("Inserting Done")
