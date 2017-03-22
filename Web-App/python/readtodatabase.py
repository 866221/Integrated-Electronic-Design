#!/usr/bin/env python

import MySQLdb

db = MySQLdb.connect("localhost", "ied", "IEDpassword", "ids")
curs = db.cursor()

try:
    curs.execute ("INSERT INTO scan values(CURRENT_DATE(), NOW(), 9786345)")

    db.commit()
    print ("Data committed")

except:
    print ("Error: the database is being rolled back")
    db.rollback()