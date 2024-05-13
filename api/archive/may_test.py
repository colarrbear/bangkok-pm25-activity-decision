import pymysql
from dbutils.pooled_db import PooledDB
from config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Optional
from fastapi import Query

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