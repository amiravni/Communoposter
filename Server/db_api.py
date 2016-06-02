
import sqlite3
import time

COMPOSTER_TBL_NAME  = "composters"
COMPOSTER_STATUS_READY_TO_TAKE = 0
COMPOSTER_STATUS_WORKING = 1
COMPOSTER_STATUS_READY_TO_PUT = 2
COMPOSTER_DOOR_STATUS_CLOSED = 0
COMPOSTER_DOOR_STATUS_OPENED = 1

COMPOSTER_TRANSACTIONS_TBL_NAME = 'user_composer_transactions'
COMPOSTER_TRANSACTIONS_TYPE_WITHDRAW = 0
COMPOSTER_TRANSACTIONS_TYPE_DEPOSIT = 1

COMPOSTER_READINGS_TBL_NAME = "composter_readings"

USERS_TBL_NAME = "users"

class db_handler():

    sql_conn = None
    sql_cursor = None
    
    def __init__(self):
        self.sql_conn = sqlite3.connect('composter.db')
        self.sql_cursor = self.sql_conn.cursor()
    
    
    def get_composters_by_user_id(self,user_id):
        composters = []
        t = (user_id,)
        self.sql_cursor.execute('SELECT * FROM %s WHERE user_id=?'%COMPOSTER_TBL_NAME, t)
        rows = self.sql_cursor.fetchall()
        
        for row in rows:
            composters.append({
                'id' : row[0],
                'user_id' : row[1],
                'composter_status' : row[2],
                'lat' : row[3],
                'lon' : row[4],
                'description' : row[5],
                'temp' : row[6],
                'humidity' : row[7],
                'weight' : row[8],
                'max_weight': row[9],
                'door_status' : row[10],
                'last_interation' : row[11]
            })
        
        return composters

    def get_composters(self):
        composters = []
        self.sql_cursor.execute('SELECT * FROM %s'%COMPOSTER_TBL_NAME)
        rows = self.sql_cursor.fetchall()
        
        for row in rows:
            composters.append({
                'id' : row[0],
                'user_id' : row[1],
                'composter_status' : row[2],
                'lat' : row[3],
                'lon' : row[4],
                'description' : row[5],
                'weight' : row[6],
                'max_weight': row[7],
                'up_door_status' : row[8],
                'down_door_status' : row[9],
                'last_interation' : row[10]
            })
        
        return composters

    def get_composters_by_id(self,composter_id):
        t = (composter_id,)
        composters = []
        self.sql_cursor.execute('SELECT * FROM %s WHERE id=?'%COMPOSTER_TBL_NAME,t)
        rows = self.sql_cursor.fetchall()
        
        for row in rows:
            composters.append({
                'id' : row[0],
                'user_id' : row[1],
                'composter_status' : row[2],
                'lat' : row[3],
                'lon' : row[4],
                'description' : row[5],
                'weight' : row[6],
                'max_weight': row[7],
                'up_door_status' : row[8],
                'down_door_status' : row[9],
                'last_interation' : row[10]
            })
        if len(composters) > 0:
            return composters[0]
        return None

    def get_users(self):
        users = []
        self.sql_cursor.execute('SELECT id,username,name,score FROM %s '%USERS_TBL_NAME)
        rows = self.sql_cursor.fetchall()
    
        for row in rows:
            users.append({
                'id' : row[0],
                'username' : row[1],
                'name':row[2],
                'score':row[3]
            })

        return users
    
    def get_user_by_username(self,username):
        users = []
        t = (username,)
        self.sql_cursor.execute('SELECT id,username,name,score FROM %s WHERE username like ? '%USERS_TBL_NAME, t)
        rows = self.sql_cursor.fetchall()
        for row in rows:
            users.append({
                'id' : row[0],
                'username' : row[1],
                'name':row[2],
                'score':row[3]
            })
        if len(users) > 0:
            return users[0]
        return None

    def get_user_by_id(self,user_id):
        users = []
        t = (user_id,)
        self.sql_cursor.execute('SELECT id,username,name,score FROM %s WHERE id=? '%USERS_TBL_NAME, t)
        rows = self.sql_cursor.fetchall()
        for row in rows:
            users.append({
                'id' : row[0],
                'username' : row[1],
                'name':row[2],
                'score':row[3]
            })
        return users[0]
    
    def insert_user(self,name,username,password):
        users_with_same_username = self.get_user_by_username(username)
        print users_with_same_username
        if users_with_same_username is not None:
            print "Error user with the same username already exist"
            return False
        self.sql_cursor.execute('INSERT INTO %s (name,username,password,score) VALUES (\'%s\',\'%s\',\'%s\',%f)' % (USERS_TBL_NAME,
                                name,username,password,0.0))
        self.sql_conn.commit()

    def update_user_score(self,user_id,score):
        t = (user_id,)
        self.sql_cursor.execute('UPDATE %s SET score=%f WHERE id=?'%(USERS_TBL_NAME,score),t)
        self.sql_conn.commit()
    
    def insert_composter(self,
                         user_id,
                         status,
                         lat,
                         lon,
                         desc,
                         max_weight,
                         up_door_status,
                         down_door_status,
                         last_interaction):
        self.sql_cursor.execute('INSERT INTO %s (user_id,status,lat,lon,description,weight,max_weight,up_door_status,down_door_status,last_interaction) VALUES (%d,%d,%f,%f,\'%s\',0,%f,%d,%d,%f)' % (COMPOSTER_TBL_NAME,user_id,status,lat,lon,desc,max_weight,up_door_status,down_door_status,last_interaction))
        self.sql_conn.commit()

    def update_composter_after_deposit(self,composter_id,weight,status):
        t = (composter_id,)
        self.sql_cursor.execute('UPDATE %s SET weight=%f,status=%d,last_interaction=%f WHERE id=?'%(COMPOSTER_TBL_NAME,weight,status,time.time()),t)
        self.sql_conn.commit()
    
    def composter_deposit(self,user_id,composter_id,weight):
        myuser = self.get_user_by_id(user_id)
        mycomposter = self.get_composters_by_id(composter_id)
        self.update_composter_after_deposit(composter_id,mycomposter['weight']+weight,mycomposter['composter_status'])
        self.update_user_score(myuser['id'],myuser['score'] + weight)
        self.sql_cursor.execute('INSERT INTO %s (user_id,composter_id,transaction_type,weight) VALUES (%d,%d,%d,%f)' % (COMPOSTER_TRANSACTIONS_TBL_NAME,user_id,composter_id,COMPOSTER_TRANSACTIONS_TYPE_DEPOSIT,weight))
        self.sql_conn.commit()

    def update_composter_after_withdraw(self,composter_id,weight,status):
        t = (composter_id,)
        self.sql_cursor.execute('UPDATE %s SET weight=%f,status=%d,last_interaction=%f WHERE id=?'%(COMPOSTER_TBL_NAME,weight,status,time.time()),t)
        self.sql_conn.commit()
    
    def composter_withdraw(self,user_id,composter_id,weight):
        myuser = self.get_user_by_id(user_id)
        mycomposter = self.get_composters_by_id(composter_id)
        self.update_composter_after_withdraw(composter_id,mycomposter['weight']-weight,mycomposter['composter_status'])
        self.update_user_score(myuser['id'],myuser['score'] - weight)
        self.sql_cursor.execute('INSERT INTO %s (user_id,composter_id,transaction_type,weight) VALUES (%d,%d,%d,%f)' % (COMPOSTER_TRANSACTIONS_TBL_NAME,user_id,composter_id,COMPOSTER_TRANSACTIONS_TYPE_DEPOSIT,weight))
        self.sql_conn.commit()


    def update_composter_after_reading(self,composter_id,weight,up_door_status,down_door_status):
        t = (composter_id,)
         
        self.sql_cursor.execute('UPDATE %s SET weight=%f WHERE id=?'%(COMPOSTER_TBL_NAME,weight),t)
        self.sql_conn.commit()

    def composter_reading_update(self,composter_id,
                                 temp1,temp2,temp3,temp4,
                                 humidity1,humidity2,humidity3,humidity4,
                                 dist1,dist2,dist3,dist4
                                 ,weight,
                                 up_door_status,down_door_status):
        #temp = (temp1 + temp2 + temp3+ temp4) / 4.0
        #humidity = (humidity1 + humidity2 + humidity3 + humidity4)
        
        self.update_composter_after_reading(composter_id,weight,up_door_status,down_door_status)
        self.sql_cursor.execute('INSERT INTO %s (composter_id,time,temp1,temp2,temp3,temp4,humidity1,humidity2,humidity3,humidity4,dist1,dist2,dist3,dist4,weight,up_door_status,down_door_status) VALUES (%d,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%d,%d)' % (COMPOSTER_READINGS_TBL_NAME,composter_id,time.time(),temp1,temp2,temp3,temp4,humidity1,humidity2,humidity3,humidity4,dist1,dist2,dist3,dist4,weight,up_door_status,down_door_status))        
        self.sql_conn.commit()

    def composter_get_last_readings(self,composter_id):
        composters = []
        t = (composter_id,)
        self.sql_cursor.execute('SELECT * FROM %s WHERE composter_id=? ORDER BY id DESC LIMIT 50'%COMPOSTER_READINGS_TBL_NAME, t)
        rows = self.sql_cursor.fetchall()
        

        for row in rows:
            composters.append({
                'id' : row[0],
                'composter_id' : row[1],
                'time' : row[2],
                'temp' : row[3:7],
                'humidity' : row[7:11],
                'dist' : row[11:15],
                'weight' : row[15],
                'up_door_status' : row[16],
                'down_door_status' : row[17]
            })
        composters.reverse()

        return composters


########################
#   Open/Close  up door   #
########################
    def update_composter_up_door_status(self,composter_id,door_status):
        t = (composter_id,)
        self.sql_cursor.execute('UPDATE %s SET up_door_status=%d WHERE id=?'%(COMPOSTER_TBL_NAME,door_status),t)

    def update_composter_after_open_up_door(self,composter_id):
        self.update_composter_up_door_status(composter_id,COMPOSTER_DOOR_STATUS_OPENED)

    def update_composter_after_close_up_door(self,composter_id):
        self.update_composter_up_door_status(composter_id,COMPOSTER_DOOR_STATUS_CLOSED)

        
    def composter_open_up_door(self,user_id,composter_id):
        self.update_composter_after_open_up_door(composter_id)
        self.sql_cursor.execute('INSERT INTO %s (user_id,composter_id,transaction_type,weight) VALUES (%d,%d,%d,%f)' % (COMPOSTER_TRANSACTIONS_TBL_NAME,user_id,composter_id,COMPOSTER_TRANSACTIONS_TYPE_DEPOSIT,0))
        self.sql_conn.commit()


    def composter_close_up_door(self,user_id,composter_id):
        self.update_composter_after_close_up_door(composter_id)
        self.sql_cursor.execute('INSERT INTO %s (user_id,composter_id,transaction_type,weight) VALUES (%d,%d,%d,%f)' % (COMPOSTER_TRANSACTIONS_TBL_NAME,user_id,composter_id,COMPOSTER_TRANSACTIONS_TYPE_DEPOSIT,0))
        self.sql_conn.commit()

########################
#   Open/Close  down door   #
########################
    def update_composter_down_door_status(self,composter_id,door_status):
        t = (composter_id,)
        self.sql_cursor.execute('UPDATE %s SET down_door_status=%d WHERE id=?'%(COMPOSTER_TBL_NAME,door_status),t)

    def update_composter_after_open_down_door(self,composter_id):
        self.update_composter_down_door_status(composter_id,COMPOSTER_DOOR_STATUS_OPENED)

    def update_composter_after_close_down_door(self,composter_id):
        self.update_composter_down_door_status(composter_id,COMPOSTER_DOOR_STATUS_CLOSED)

        
    def composter_open_down_door(self,user_id,composter_id):
        self.update_composter_after_open_down_door(composter_id)
        self.sql_cursor.execute('INSERT INTO %s (user_id,composter_id,transaction_type,weight) VALUES (%d,%d,%d,%f)' % (COMPOSTER_TRANSACTIONS_TBL_NAME,user_id,composter_id,COMPOSTER_TRANSACTIONS_TYPE_DEPOSIT,0))
        self.sql_conn.commit()


    def composter_close_down_door(self,user_id,composter_id):
        self.update_composter_after_close_down_door(composter_id)
        self.sql_cursor.execute('INSERT INTO %s (user_id,composter_id,transaction_type,weight) VALUES (%d,%d,%d,%f)' % (COMPOSTER_TRANSACTIONS_TBL_NAME,user_id,composter_id,COMPOSTER_TRANSACTIONS_TYPE_DEPOSIT,0))
        self.sql_conn.commit()
        
        
    def close(self):
        self.sql_conn.commit()
        self.sql_conn.close()
        self.sql_conn = None
        self.sql_cursor = None
