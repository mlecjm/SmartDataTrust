"""
Author          : Neda Peyrone
Create Date     : 25-06-2021
File            : service_exception.py
Purpose         : -
"""

class ServiceException(Exception):
  def __init__(self, msg):
    self.msg = msg

  def __str__(self):
    return repr(self.msg)