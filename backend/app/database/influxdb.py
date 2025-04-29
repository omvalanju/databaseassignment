# app/database/influxdb.py

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import current_app

def _get_client() -> InfluxDBClient:
    return InfluxDBClient(
        url=current_app.config['INFLUX_URL'],
        token=current_app.config['INFLUX_TOKEN'],
        org=current_app.config['INFLUX_ORG']
    )

def get_write_api():
    client = _get_client()
    return client.write_api(write_options=SYNCHRONOUS)

def get_query_api():
    client = _get_client()
    return client.query_api()

def get_bucket() -> str:
    return current_app.config['INFLUX_BUCKET']

def get_org() -> str:
    return current_app.config['INFLUX_ORG']
