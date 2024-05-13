import re
#
# import pymysql
# import pandas as pd
# from dbutils.pooled_db import PooledDB
# # from fastapi import FastAPI, HTTPException
# from config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
# from datetime import datetime
#
# # sys.path.append(OPENAPI_STUB_DIR)
# # from swagger_server import models
#
# pool = PooledDB(
#     creator=pymysql,
#     host=DB_HOST,
#     user=DB_USER,
#     password=DB_PASSWD,
#     database=DB_NAME,
#     maxconnections=1,
#     blocking=True,
# )

# Load data from the database and CSV file
# db_data = pd.read_sql_query("SELECT * FROM AQMTHAI", pool.connection())
# csv_data = pd.read_csv("response_clean.csv")

# csv_timestamp = csv_data["datetime"][0]

# # Convert CSV timestamp to the same format as the database timestamp
# csv_datetime = datetime.strptime(csv_timestamp, "%d/%m/%Y, %H:%M:%S")
# formatted_csv_timestamp = csv_datetime.strftime("%Y-%m-%d %H:%M:%S")

# permanent update datetime into database format
# csv_data['datetime'] = pd.to_datetime(csv_data['datetime'], format='%d/%m/%Y, %H:%M:%S')
# csv_data['datetime'] = csv_data['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
#
# csv_data.to_csv("response_clean.csv", index=False)

# "permanent" clean the data -> district must have only "เขต" + thai district name
# original_location = csv_data["district"]
# # Chatuchak 10900 จตุจักร -> เขตจตุจักร
# cleaned_location = []
#
# for location in original_location:
#     # get only thai district
#     thai_dist = re.split(r'\d+', location)[1]
#     cleaned_location.append(f'เขต{thai_dist}')
# # remove spaces
# cleaned_location = [location.replace(" ", "") for location in cleaned_location]
# csv_data["district"] = cleaned_location
# csv_data.to_csv("response_clean.csv", index=False)
# print(cleaned_location)

