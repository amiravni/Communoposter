# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 11:25:54 2016

@author: ubuser
"""

import db_api
from db_api import db_handler
import time

db_con = db_handler()

db_con.insert_user('the dude','thedude','mypassword')
db_con.insert_user('the other dude','theotherdude','mypassword')
myuser = db_con.get_user_by_username('thedude')

mycomposter =db_con.get_composters_by_id(1)
print myuser
"""
db_con.insert_composter(myuser['id'],
                         db_api.COMPOSTER_STATUS_READY_TO_PUT,
                         32.142,
                         34.512,
                         "My composter is the best",
                         1043.12,
                         db_api.COMPOSTER_DOOR_STATUS_CLOSED,
                         time.time())
"""
print "#"*50
print 'Users'
print "#"*50
print db_con.get_users()
print "#"*50
print 'composters'
print "#"*50
print db_con.get_composters()
print "#"*50
print 'user %s composters' % myuser['name']
print "#"*50
print db_con.get_composters_by_user_id(myuser['id'])
if mycomposter is not None:
    db_con.composter_deposit(myuser['id'],mycomposter['id'],0.53)
    db_con.composter_withdraw(myuser['id'],mycomposter['id'],0.06)

db_con.close()