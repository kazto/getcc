#! /usr/bin/env python3

import datetime

def get_today():
    today = datetime.datetime.now()
    todaystr = "{0.year}-{0.month:02d}-{0.day:02d}".format(today)
    return(todaystr)

