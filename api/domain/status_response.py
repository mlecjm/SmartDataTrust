"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : status_response.py
Purpose         : -
"""


class StatusResponse(object):
  code: str
  desc: str

  def __init__(self, code, desc):
    self.code = code
    self.desc = desc