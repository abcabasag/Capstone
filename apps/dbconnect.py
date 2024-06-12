import pandas as pd
import psycopg2

def getdblocation():
    db = psycopg2.connect(
        host="localhost",
        database="capstonedb",
        user="postgres",
        port=5432,
        password="password",
    )
    return db

def modifydatabase(sql, values):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()

def querydatafromdatabase(sql, values, dfcolumns):
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows

def username_exists(username):
    db = getdblocation()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE user_name = %s", (username,))
    count = cur.fetchone()[0]
    db.close()
    return count > 0

def get_latest_request_class_id():
    db = getdblocation()
    cur = db.cursor()
    cur.execute("SELECT max(Request_class_id) FROM Request_Class")
    latest_request_class_id = cur.fetchone()
    db.close()
    if latest_request_class_id:
        return latest_request_class_id[0]
    else:
        return None
    
def get_latest_request_number():
    db = getdblocation()
    cur = db.cursor()
    cur.execute("SELECT Request_number FROM Request_Class ORDER BY Request_Class_ID DESC LIMIT 1")
    latest_request_number = cur.fetchone()
    db.close()
    if latest_request_number:
        return latest_request_number[0]
    else:
        return None
    
def get_latest_email():
    db = getdblocation()
    cur = db.cursor()
    cur.execute("SELECT email FROM Request_Class ORDER BY Request_Class_ID DESC LIMIT 1")
    latest_email = cur.fetchone()
    db.close()
    if latest_email:
        return latest_email[0]
    else:
        return None
