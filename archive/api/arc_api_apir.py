import pymysql
import pandas as pd
from dbutils.pooled_db import PooledDB
# from fastapi import FastAPI, HTTPException
from config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME

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
print(pair_data)


# app = Flask(__name__)
#
# @app.route('/pair_with_aqmthai', methods=['GET'])
# def pair_with_aqmthai():
#     return jsonify(pair_data)
#
# if __name__ == '__main__':
#     app.run(debug=True)