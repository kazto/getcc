#! /usr/bin/env python

import sys
import os.path
import subprocess as sp
import datetime

cc = sys.argv[1]

today = datetime.datetime.now()
todaystr = "{0.year}-{0.month:02d}-{0.day:02d}".format(today)
dbname = "{}-{}.db".format(cc, todaystr)

print(dbname)

if not os.path.exists(dbname):
    sp.call(["python", "init_table.py", dbname])

sp.call(["python", "getcc.py", cc])

