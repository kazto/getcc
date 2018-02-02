#! /usr/bin/env python3

import sys
import sqlite3
from contextlib import closing
import datetime as dt

#stride = int(sys.argv[2])

def time_to_list(date):
    d, t = date.split(" ")
    d = [int(x) for x in d.split("-")]
    t = [int(x) for x in t.split(":")]
    return(d + t)

def modify_time(date):
    time = yield( time_to_list(date) )
    return(time.strftime("%Y-%m-%d %H:%M:%S"))

def floor_sec(date):
    yr, mt, dy, hr, mn, sc = time_to_list(date)
    return(dt.datetime(yr, mt, dy, hr, mn, 0))

def ceil_sec(date):
    yr, mt, dy, hr, mn, sc = time_to_list(date)
    return(
        dt.datetime(yr, mt, dy, hr, mn, 0) +
        dt.timedelta(seconds= 60 if sc > 0 else 0)
    )

t = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(t)
print(time_to_list(t))
print(floor_sec(t))
print(ceil_sec(t))





# with closing(sqlite3.connect(sys.argv[1])) as conn:
#     csr = conn.cursor()

