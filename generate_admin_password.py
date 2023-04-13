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
if (("admins",) in tables):
    cur.execute("DROP TABLE admins;")
cur.execute("CREATE TABLE admins (id NUMERIC(8) NOT NULL, key_ CHAR(128) NOT NULL, PRIMARY KEY (id));")

for id in range(1, 10):
    password = "password"
    cur.execute(f"INSERT INTO admins (id, key_) VALUES ({id}, '{password}');")

mydb.commit()