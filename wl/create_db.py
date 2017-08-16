import mysql.connector
import os


conn = mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
)
try:
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE dougandmiriam')
    cursor.execute('USE dougandmiriam')
    cursor.execute("""CREATE TABLE item (
    id INT PRIMARY KEY NOT NULL,
    title VARCHAR(256) NOT NULL,
    description VARCHAR(1024) NOT NULL
    )""")
    cursor.execute("""CREATE TABLE image (
    item_id INT NOT NULL,
    image VARCHAR(256) NOT NULL,
    link VARCHAR(256) NOT NULL,
    sort_order INT NOT NULL,
    INDEX(item_id)
    )""")
    cursor.execute("""CREATE TABLE claim (
    item_id INT NOT NULL,
    email VARCHAR(256) NOT NULL,
    time DATE NOT NULL,
    note VARCHAR(1024) NOT NULL,
    INDEX(item_id)
    )""")
finally:
    conn.close()
