from enum import Enum

"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : message_code.py
Purpose         : -
"""


class MessageCode(Enum):
  def __str__(self):
    return str(self.value)

  SUCCESS = 'Service Success.'
  ERROR_INVALID_PARAM = 'Invalid parameter.'
  ERROR_CONTRACT_LOGIC = 'Invalid smart contract logic.'
  UNKNOWN_ERROR = 'Unknown error'