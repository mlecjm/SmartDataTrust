import json
import enum
from datetime import date
from datetime import time
from datetime import datetime

"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : json_util.py
Purpose         : -
"""


def to_serializable(val):
  """JSON serializer for objects not serializable by default"""
  
  if isinstance(val, (datetime, date, time)):
    return val.isoformat()
  elif isinstance(val, enum.Enum):
    return val.value
  elif hasattr(val, '__dict__'):
    return val.__dict__


def to_json(data):
  """Converts object to JSON formatted string"""
  return json.dumps(data, default=to_serializable)
