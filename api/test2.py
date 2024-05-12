import pymysql
from dbutils.pooled_db import PooledDB
from config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from datetime import datetime

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


@app.get("/api/air_quality")
async def get_air_quality() -> list[AirQuality]:
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT datetime, district, location, aqi, level FROM airbkk
        """)
        result = [AirQuality(ts=ts, district=district, location=location,
                             aqi=aqi, level=level)
                  for ts, district, location, aqi, level in cs.fetchall()]
    return result
