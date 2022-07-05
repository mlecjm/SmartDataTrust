"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : header.py
Purpose         : -
"""


class Header(object):
  request_id: str
  caller_id: str
  transaction_date: str

  def __init__(
    self,
    request_id=None,
    caller_id=None,
    transaction_date=None
  ):
    super(Header, self).__init__()
    self.request_id = request_id
    self.caller_id = caller_id
    self.transaction_date = transaction_date
