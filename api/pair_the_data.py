import pymysql
import pandas as pd
from dbutils.pooled_db import PooledDB
# from fastapi import FastAPI, HTTPException
from config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from datetime import datetime

# sys.path.append(OPENAPI_STUB_DIR)
# from swagger_server import models

pool = PooledDB(
    creator=pymysql,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWD,
    database=DB_NAME,
    maxconnections=1,
    blocking=True,
)

# Load data from the database and CSV file
def get_data_from_db():
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM AQMTHAI")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_response_from_csv():
    with open('response_clean.csv', 'r') as f:
        # convert datetime to same format as in the database
        data = pd.read_csv(f)
        data['timestamp'] = pd.to_datetime(data['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        data = data.to_dict(orient='records')
    return data

# Pair the data from the database and CSV file
def pair_data():
    data = get_data_from_db()
    response = get_response_from_csv()
    paired_data = []
    for d in data:
        for r in response:
            if d[1] == r['timestamp']:
                paired_data.append((d[0], r['timestamp'], r['value'], r['response']))
    return paired_data


# print to check the output
print(pair_data())