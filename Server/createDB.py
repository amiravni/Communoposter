# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/ubuser/.spyder2/.temp.py
"""

import sqlite3 as lite
import sys
import os
con = None

try:
    os.system('rm composter.db')

    con = lite.connect('composter.db')
    sql_cursor = con.cursor()
    
    sql_cursor.execute('''CREATE TABLE users
                 (id Integer PRIMARY KEY AUTOINCREMENT,
                 name TEXT,username TEXT, password TEXT,score FLOAT)''')
    
    # create table
    #status - ready_to_take,working-dnd, ready_to_put
    #door-status - open/closed
    sql_cursor.execute('''CREATE TABLE composters
                 (id Integer PRIMARY KEY AUTOINCREMENT,
                 user_id INT, status INT,
                 lat FLOAT, lon FLOAT, description TEXT, 
                 weight FLOAT,
                 max_weight FLOAT,
                 up_door_status INT,
                 down_door_status INT,
                 last_interaction DOUBLE)''')
    
    #transaction_type - deposit/withdraw
    sql_cursor.execute('''CREATE TABLE user_composer_transactions
                 (id Integer PRIMARY KEY AUTOINCREMENT,
                 user_id INT, composter_id INT, transaction_type INT, weight FLOAT )''')
                 

    sql_cursor.execute('''CREATE TABLE composter_readings
                 (id Integer PRIMARY KEY AUTOINCREMENT,
                 composter_id INT, time DOUBLE , 
                 temp1 FLOAT ,temp2 FLOAT,temp3 FLOAT,temp4 FLOAT,
                 humidity1 FLOAT,humidity2 FLOAT,humidity3 FLOAT,humidity4 FLOAT,
                 dist1 FLOAT,dist2 FLOAT, dist3 FLOAT, dist4 FLOAT,
                 weight FLOAT,up_door_status INT,down_door_status INT )''')

except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()