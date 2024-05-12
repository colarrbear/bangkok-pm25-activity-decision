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


class TempValue(BaseModel):
    ts: datetime
    temp: float


class Pm25Value(BaseModel):
    ts: datetime
    pm25: int


@app.get("/api/temp")
async def get_temp() -> list[TempValue]:
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT ts, temp FROM temp
        """)
        result = [TempValue(ts=ts, temp=temp) for ts, temp in cs.fetchall()]
    return result


@app.get("/api/pm25")
async def get_pm25() -> list[Pm25Value]:
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT ts, pm25 FROM pm25
        """)
        result = [Pm25Value(ts=ts, pm25=pm25) for ts, pm25 in cs.fetchall()]
    return result