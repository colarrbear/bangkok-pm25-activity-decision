import pymysql
from dbutils.pooled_db import PooledDB
from config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Optional
from fastapi import Query
import pandas as pd
from typing import List

pool = PooledDB(creator=pymysql,
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWD,
                database=DB_NAME,
                maxconnections=1,
                blocking=True)
app = FastAPI()


class AirQuality(BaseModel):
    ts: datetime
    district: str
    location: str
    aqi: int
    level: str


class DecisionAQMTHAI(BaseModel):
    ts: datetime
    district: str
    aqi: int
    current_AQI: int
    dicision: str


@app.get("/api/air_quality")
async def get_air_quality(
    district: Optional[str] = Query(None, description="Filter by district"),
    location: Optional[str] = Query(None, description="Filter by location")
) -> list[AirQuality]:
    try:
        with pool.connection() as conn, conn.cursor() as cs:
            query = """
                SELECT datetime, district, location, aqi, level FROM airbkk
            """
            if district:
                query += f" WHERE district = '{district}'"
                if location:
                    query += f" AND location = '{location}'"
            elif location:
                query += f" WHERE location = '{location}'"

            cs.execute(query)
            result = [AirQuality(ts=ts, district=district, location=location, aqi=aqi, level=level)
                      for ts, district, location, aqi, level in cs.fetchall()]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/decision_AQMTHAI_based")
async def get_decision_AQMTHAI_based(
    district: Optional[str] = Query(None, description="Filter by district"),
    location: Optional[str] = Query(None, description="Filter by location")
) -> list[AirQuality]:
    try:
        with pool.connection() as conn, conn.cursor() as cs:
            query = """
                SELECT datetime, district, aqi FROM AQMTHAI
            """
            if district:
                query += f" WHERE district = '{district}'"
                # if location:
                #     query += f" AND location = '{location}'"
            elif location:
                query += f" WHERE location = '{location}'"

            cs.execute(query)
            result = [AirQuality(ts=ts, district=district, aqi=aqi,)
                      for ts, district, aqi, in cs.fetchall()]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import pymysql
from dbutils.pooled_db import PooledDB
from config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Optional
from fastapi import Query
import pandas as pd
from typing import List


pool = PooledDB(creator=pymysql,
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWD,
                database=DB_NAME,
                maxconnections=1,
                blocking=True)
app = FastAPI()


class AirQuality(BaseModel):
    ts: datetime
    district: str
    location: str
    aqi: int
    level: str


class DecisionAQMTHAI(BaseModel):
    ts: datetime
    district: str
    aqi: int
    current_AQI: int
    dicision: str


@app.get("/api/air_quality")
async def get_air_quality(
    district: Optional[str] = Query(None, description="Filter by district"),
    location: Optional[str] = Query(None, description="Filter by location")
) -> list[AirQuality]:
    try:
        with pool.connection() as conn, conn.cursor() as cs:
            query = """
                SELECT datetime, district, location, aqi, level FROM airbkk
            """
            if district:
                query += f" WHERE district = '{district}'"
                if location:
                    query += f" AND location = '{location}'"
            elif location:
                query += f" WHERE location = '{location}'"

            cs.execute(query)
            result = [AirQuality(ts=ts, district=district, location=location, aqi=aqi, level=level)
                      for ts, district, location, aqi, level in cs.fetchall()]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/decision_AQMTHAI_based")
async def get_decision_AQMTHAI_based(
    district: Optional[str] = Query(None, description="Filter by district"),
    location: Optional[str] = Query(None, description="Filter by location")
) -> list[AirQuality]:
    try:
        with pool.connection() as conn, conn.cursor() as cs:
            query = """
                SELECT datetime, district, aqi FROM AQMTHAI
            """
            if district:
                query += f" WHERE district = '{district}'"
                # if location:
                #     query += f" AND location = '{location}'"
            elif location:
                query += f" WHERE location = '{location}'"

            cs.execute(query)
            result = [AirQuality(ts=ts, district=district, aqi=aqi,)
                      for ts, district, aqi, in cs.fetchall()]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pair_with_aqmthai")
async def pair_with_aqmthai(
    district: Optional[str] = Query(None, description="Filter by district"),
    location: Optional[str] = Query(None, description="Filter by location")
) -> list[DecisionAQMTHAI]:
    try:
        paired_data = []

        # Load data from the database
        with pool.connection() as conn, conn.cursor() as cs:
            query = """
                SELECT datetime, district, aqi FROM AQMTHAI
            """
            if district:
                query += f" WHERE district = '{district}'"
            elif location:
                query += f" WHERE location = '{location}'"

            cs.execute(query)
            db_data = cs.fetchall()



        # Load data from the CSV file
        csv_data = pd.read_csv("response_clean.csv")
        csv_data['datetime'] = pd.to_datetime(csv_data['datetime'])

        # Iterate through each record in the database data
        for db_row in db_data:
            db_timestamp, db_location, db_aqi = db_row

            # Find matching rows in the CSV data
            matching_csv_rows = csv_data[
                (csv_data['datetime'] >= db_timestamp - pd.Timedelta(hours=1)) &
                (csv_data['datetime'] <= db_timestamp + pd.Timedelta(hours=1)) &
                csv_data['district'].str.contains(db_location)
                ]

            if not matching_csv_rows.empty:
                for _, csv_row in matching_csv_rows.iterrows():
                    csv_current_aqi = csv_row['current_AQI']
                    csv_go_outside = csv_row['go_outside']

                    # Create an instance of DecisionAQMTHAI and append it to the list
                    paired_data.append(DecisionAQMTHAI(
                        ts=db_timestamp,
                        district=db_location,
                        aqi=db_aqi,
                        current_AQI=csv_current_aqi,
                        decision=csv_go_outside  # Assuming 'go_outside' represents the decision
                    ))

        return paired_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
