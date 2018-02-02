#! /usr/bin/env python3

import sys
import sqlite3
import datetime
from zaifapi.impl import ZaifPublicApi
from contextlib import closing
from getccutil import get_today

api = ZaifPublicApi()

cc = sys.argv[1]
todaystr = get_today()
dbname = "{}-{}.db".format(cc, todaystr)

def exist_entry(csr, tid):
    csr.execute("select tid from trades where tid = ?", (tid,))
    return(len(csr.fetchall()) > 0)

def gen_table(csr, table):
    pairs_table = {}
    for row in csr.execute("select * from {};".format(table)):
        pairs_table[row[1]] = row[0]
    return(pairs_table)

with closing(sqlite3.connect(dbname)) as conn:
    csr = conn.cursor()
    pairs_table = gen_table(csr, "currency_pairs")
    trade_type_table = gen_table(csr, "trade_types")

    if len(pairs_table) == 0 or len(trade_type_table) == 0:
        raise RuntimeError("table is empty!")

    count_add = 0
    count_drop = 0

    trades = api.trades(cc + "_jpy")
    for row in trades:
        if not exist_entry(csr, row["tid"]):
            count_add += 1
            csr.execute(
                "insert into trades values(?, ?, ?, ?, ?, ?)",
                (
                    row["date"], row["price"], row["amount"], row["tid"],
                    pairs_table[row["currency_pair"]],
                    trade_type_table[row["trade_type"]]
                )
            )
        else:
            count_drop += 1
    print("{}: add => {}, drop => {}".format(cc, count_add, count_drop))

    conn.commit()
