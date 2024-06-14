import os
import pandas as pd
import psycopg2

def getdblocation():
    DATABASE = os.environ['DATABASE']
    db = psycopg2.connect(DATABASE, sslmode='require')
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
    cur.execute("SELECT max(request_class_id) FROM request_class")
    latest_request_class_id = cur.fetchone()
    db.close()
    if latest_request_class_id:
        return latest_request_class_id[0]
    else:
        return None
    
def get_latest_request_number():
    db = getdblocation()
    cur = db.cursor()
    cur.execute("SELECT request_number FROM request_class ORDER BY request_class_id DESC LIMIT 1")
    latest_request_number = cur.fetchone()
    db.close()
    if latest_request_number:
        return latest_request_number[0]
    else:
        return None
    
def get_latest_email():
    db = getdblocation()
    cur = db.cursor()
    cur.execute("SELECT email FROM request_Class ORDER BY request_Class_id DESC LIMIT 1")
    latest_email = cur.fetchone()
    db.close()
    if latest_email:
        return latest_email[0]
    else:
        return None

def get_requestor_name_by_email(request_class_id):
    db = getdblocation()
    cur = db.cursor()
    cur.execute("SELECT rc_first_name, rc_last_name FROM request_class WHERE request_class_id = %s", (request_class_id,))
    requestor = cur.fetchone()
    db.close()
    if requestor:
        return f"{requestor[0]} {requestor[1]}"
    else:
        return None
