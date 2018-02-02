#! /usr/bin/env python3

import sys
import json
import sqlite3
from contextlib import closing
import requests
import datetime

# cc = sys.argv[1]

# today = datetime.datetime.now()
# todaystr = "{0.year}-{0.month:02d}-{0.day:02d}".format(today)
# dbname = "{}-{}.db".format(cc, todaystr)

dbname = sys.argv[1]

data = requests.get("https://api.zaif.jp/api/1/currency_pairs/all").text

pairs = json.loads(data)

with closing(sqlite3.connect(dbname)) as conn:
    csr = conn.cursor()
    csr.execute("create table currency_pairs(id int primary key, currency_pair text);")

    for row in pairs:
        print((row['id'], row['currency_pair']))
        csr.execute(
            "insert into currency_pairs values(?, ?);",
            (row['id'], row['currency_pair'])
            )

    csr.execute("create table trade_types(id int primary key, trade_type text);")
    csr.execute("insert into trade_types values(0, 'ask');")
    csr.execute("insert into trade_types values(1, 'bid');")

    csr.execute("""
CREATE TABLE trades(
  date int,
  price int,
  amount real,
  tid int primary key,
  currency_pair_id int,
  trade_type_id int
);
""")
    conn.commit()


