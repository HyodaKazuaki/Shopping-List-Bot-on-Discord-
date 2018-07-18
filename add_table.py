#!/usr/bin/env python3

import sqlite3
from contextlib import closing

dbname = 'database.db'

with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()
    create_table = '''
        CREATE TABLE list(
            id          INTEGER PRIMARY KEY,
            item        VARCHAR(1000),
            insert_time TIMESTAMP DEFAULT (DATETIME('now','localtime'))
            )'''
    c.execute(create_table)

print("Table has been created successfully.")