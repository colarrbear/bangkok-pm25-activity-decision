import pymysql
import pandas as pd
from dbutils.pooled_db import PooledDB
from flask import Flask, jsonify
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
    # maxconnections=1,
    blocking=True,
)


# Load data from the database and CSV file
db_data = pd.read_sql_query("SELECT * FROM AQMTHAI", pool.connection())
csv_data = pd.read_csv("response_clean.csv")
# csv_data = pd.read_csv("api/response_clean.csv")
# print(type(csv_data["datetime"][0]))
# to datetime
csv_data['datetime'] = pd.to_datetime(csv_data['datetime'])
csv_but_timestamp = csv_data['datetime']
# print(type(csv_data["datetime"][0]))

# pair data (AQI index "aqi" from database, AQI index ("current_AQI") from response and
# Decision to go outside ("go_outside")) based on timestamp and location

pair_data = []
# if location in database is the same as location in response
# and timestamp in database is the same as timestamp in response
# then pair the data

# Iterate through each record in the database data
for db_index, db_row in db_data.iterrows():
    db_timestamp = db_row['datetime']
    db_location = db_row['district']
    db_aqi = db_row['aqi']

    # Check if there's a corresponding record in the CSV data with the same or near timestamp and location
    matching_csv_rows = csv_data[
        (csv_but_timestamp >= db_timestamp - pd.Timedelta(hours=1)) &  # Example: Check within 1 hour window
        (csv_but_timestamp <= db_timestamp + pd.Timedelta(hours=1)) &  # Example: Check within 1 hour window
        csv_data['district'].str.contains(db_location)
        ]

    # If there are matching records in the CSV data
    if not matching_csv_rows.empty:
        for csv_index, csv_row in matching_csv_rows.iterrows():
            csv_current_aqi = csv_row['current_AQI']
            csv_go_outside = csv_row['go_outside']

            # Pair the data (database AQI, response current AQI, and go outside decision)
            pair_data.append({
                'timestamp': db_timestamp,
                'location': db_location,
                'aqi': db_aqi,
                'current_AQI': csv_current_aqi,
                'go_outside': csv_go_outside
            })

# Now pair_data contains the paired records based on timestamp and location
# print(pair_data)

from fastapi import FastAPI
from typing import List, Optional

# Create a FastAPI app instance
app = FastAPI()

# Define a route to return the paired data
@app.get("/pair_data/")
async def get_pair_data(location: Optional[str] = None, timestamp: Optional[str] = None):
    # If location and timestamp are provided, filter the pair_data
    if location and timestamp:
        filtered_data = [entry for entry in pair_data if entry['location'] == location and entry['timestamp'] == timestamp]
        return filtered_data
    else:
        return pair_data

# Run the FastAPI app using Uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
