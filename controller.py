import connexion
import six
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

# from swagger_server.models.api import API  # noqa: E501
# from swagger_server.models.locationto_decision import LocationtoDecision  # noqa: E501
# from swagger_server.models.pmapi import PMAPI  # noqa: E501
# from swagger_server import util


def controller_get_api():  # noqa: E501
    """Returns a list of API.

     # noqa: E501


    :rtype: List[API]
    """
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT id, datetime, aqi
            FROM airbkk
            """)
        # cs.execute("SELECT district, aqi FROM airbkk LEFT JOIN AQMTHAI ON airbkk.datetime = AQMTHAI.datetime")
        # result = [models.BasinShort(basin_id, name) for basin_id, name in
        #           cs.fetchall()]
        result = [models.API(ts=ts, district=district, aqi=aqi)
                  for ts, district, aqi in cs.fetchall()]
    return result


def controller_get_locationto_decision():  # noqa: E501
    """Returns a list of Decision.

     # noqa: E501


    :rtype: List[LocationtoDecision]
    """
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT basin_id, ename, area
            FROM basin
            WHERE basin_id=%s
            """, [basin_id])
        result = cs.fetchone()
    if result:
        basin_id, name, area = result
        return models.BasinFull(basin_id, name, area)
    else:
        abort(404)


def controller_get_pm_api():  # noqa: E501
    """Returns a list of PM.

     # noqa: E501


    :rtype: List[PMAPI]
    """
    with pool.connection() as conn, conn.cursor() as cs:
        cs.execute("""
            SELECT station_id, s.ename
            FROM station s
            INNER JOIN basin b ON s.basin_id=b.basin_id
            WHERE b.basin_id=%s
            """, [basin_id])
        result = [models.StationShort(station_id, name) for station_id, name in cs.fetchall()]
    return result

