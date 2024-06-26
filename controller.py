# i
import connexion
import six
import csv
import sys
from flask import abort
import pymysql
from dbutils.pooled_db import PooledDB
from config import OPENAPI_STUB_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME

sys.path.append(OPENAPI_STUB_DIR)
from swagger_server import models

pool = PooledDB(creator=pymysql,
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWD,
                database=DB_NAME,
                maxconnections=1,
                blocking=True)


from swagger_server.models.api import API  # noqa: E501
from swagger_server.models.locationto_decision import LocationtoDecision  # noqa: E501
from swagger_server.models.pmapi import PMAPI  # noqa: E501
from swagger_server import util

def controller_get_api():  # noqa: E501
    """Returns a list of API.

     # noqa: E501


    :rtype: List[API]
    """
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT AQMTHAI.id, AQMTHAI.datetime, AQMTHAI.district, AQMTHAI.aqi
            FROM AQMTHAI
            """)
        result = [models.API(id=id, ts=ts, district=district, aqi=aqi) for
                  id, ts, district, aqi in cs.fetchall()]
    return result


def controller_get_locationto_decision():  # noqa: E501
    """Returns a list of Decision.

     # noqa: E501


    :rtype: List[LocationtoDecision]
    """
    # from response_clean.csv: "district" and "decision"
    # read csv file
    data = []
    with open('response_clean.csv', 'r', encoding='utf-8',
              errors='ignore') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for row in csv_reader:
            district = row[4]
            current_AQI = row[12]
            go_outside = row[16]
            ts = row[0]
            data.append(
                models.LocationtoDecision(aqi=current_AQI, decision=go_outside,
                                          district=district, ts=ts))
    return data


def controller_get_pm_api():  # noqa: E501
    """Returns a list of PM.

     # noqa: E501


    :rtype: List[PMAPI]
    """
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT datetime, pm25, district
            FROM airbkk
            """)
        result = [models.PMAPI(ts=ts, district=district, pm25=pm25) for
                  ts, pm25, district in cs.fetchall()]
    return result
