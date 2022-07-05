import json
from typing import Optional

"""
Author          : Neda Peyrone
Create Date     : 24-06-2021
File            : rest_client.py
Purpose         : -
"""


class RestClient:

  def __init__(self, url, session, headers, payload: Optional[any] = None) -> None:
    self.url = url
    self.session = session
    self.headers = headers
    self.payload = payload

  def post(self):
    return self.session.post(
      url=self.url,
      headers=self.init_headers(),
      data=json.dumps(self.payload),
      verify=False
    )

  def get(self):
    return self.session.get(
      url=self.url,
      headers=self.init_headers(),
      verify=False
    )

  def init_headers(self):
    d = {"Content-Type": "application/json"}
    for key, value in self.headers.items():
      d[key] = value
    return d
