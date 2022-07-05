import tzlocal
from datetime import datetime

"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : date_util.py
Purpose         : -
"""

def to_timestamp(s: str):
  dt = datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%f%z') # 2021-09-23T20:11:54.893137+07:00

  # Convert datetime to seconds since the Epoch
  ts = int(dt.strftime('%s'))
  return ts

def to_isoformat(ts: int):
  local_tz = tzlocal.get_localzone()
  return datetime.fromtimestamp(ts, local_tz).isoformat()
