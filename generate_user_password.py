import os
import hashlib
from utils import generate_key
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="Password@1234",
  database="hostelmng"
)

# Creating the database table users
cur = mydb.cursor()
cur.execute("SHOW TABLES;")
tables = cur.fetchall()
print(tables)
if (("users",) in tables):
    cur.execute("DROP TABLE users;")
cur.execute("CREATE TABLE users (id NUMERIC(8) NOT NULL, key_ CHAR(128) NOT NULL, PRIMARY KEY (id));")

for id in range(20000000, 20000300):
    password = "password"
    key = generate_key(password)
    print(key)
    cur.execute(f"INSERT INTO users (id, key_) VALUES ({id}, '{key}');")

mydb.commit()