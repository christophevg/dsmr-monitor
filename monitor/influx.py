from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import os

URL    = os.environ.get("INFLUX_URL")
TOKEN  = os.environ.get("INFLUX_TOKEN")
BUCKET = os.environ.get("INFLUX_BUCKET")
ORG    = os.environ.get("INFLUX_ORG")

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS

import datetime

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)

write_api = client.write_api(write_options=ASYNCHRONOUS)

def influxdb_write(measurement, points):
  records = []
  for timestamp, values in points:
    point = Point(measurement).time(timestamp)
    for name, value in values.items():
      point.field(name, value)
    records.append(point)
  async_result = write_api.write(bucket=BUCKET, record=records)
  async_result.get()

if __name__ == "__main__":
  import random
  import time

  def add_point():
    now = datetime.datetime.utcnow()
    value1 = random.uniform(1500, 1900)
    value2 = random.uniform(150, 190)
    print(value1, value2)
    influxdb_write("test", [
      (now, {
        "value1" : value1,
        "value2" : value2
      })
    ])

  def query():
    query_api = client.query_api()
    tables = query_api.query('from(bucket:"' + BUCKET + '") |> range(start: -10m)')
    for table in tables:
      print(table)
      for row in table.records:
        print (row.values)

  # generate/insert points every second
  try:
    while True:
      time.sleep(1)
      add_point()
  except KeyboardInterrupt:
    pass

  query()

  client.close()
