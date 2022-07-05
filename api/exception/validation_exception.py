"""
Author          : Neda Peyrone
Create Date     : 02-07-2021
File            : validation_exception.py
Purpose         : -
"""

class ValidationException(Exception):
  def __init__(self, msg):
    self.msg = msg

  def __str__(self):
    return repr(self.msg)