"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : data_access_response.py
Purpose         : -
"""


class DataAccessResponse(object):
  response_id: str
  request_id: str
  accepted_flag: str
  accepted_message: str
  create_date: str
  responder_url: str

  def __init__(self,
    response_id=None,
    request_id=None,
    accepted_flag=None, 
    accepted_message=None, 
    create_date=None,
    responder_url=None
  ):
    super(DataAccessResponse, self).__init__()
    self.response_id = response_id
    self.request_id = request_id
    self.accepted_flag = accepted_flag
    self.accepted_message = accepted_message
    self.create_date = create_date
    self.responder_url = responder_url