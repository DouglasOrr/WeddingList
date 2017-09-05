"""From empty, create the wedding list database.
"""

import os
from . import util


with util.UsingConn(util.connect(database=None)) as conn, \
     util.UsingCursor(conn) as cursor:

    cursor.execute('CREATE DATABASE %s' % os.environ['DB_DATABASE'])
    cursor.execute('USE %s' % os.environ['DB_DATABASE'])
    cursor.execute("""CREATE TABLE item (
    id INT PRIMARY KEY NOT NULL,
    title VARCHAR(256) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    value FLOAT NOT NULL
    )""")
    cursor.execute("""CREATE TABLE image (
    item_id INT NOT NULL,
    path VARCHAR(512) NOT NULL,
    link VARCHAR(512) NOT NULL,
    INDEX(item_id)
    )""")
    cursor.execute("""CREATE TABLE claim (
    item_id INT PRIMARY KEY NOT NULL,
    name VARCHAR(256) NOT NULL,
    email VARCHAR(256) NOT NULL,
    time DATE NOT NULL,
    note VARCHAR(1024) NOT NULL
    )""")
    conn.commit()
