"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : data_access_request.py
Purpose         : -
"""


class DataAccessRequest(object):
  request_id: str
  pseudonym: str
  consent_code: str
  consent_version: int
  responder_id: str
  data_transfer_url: str
  create_date: str

  def __init__(self,
    request_id=None,
    pseudonym=None, 
    consent_code=None, 
    consent_version=None,
    responder_id=None,
    data_transfer_url=None,
    create_date=None
  ):
    super(DataAccessRequest, self).__init__()
    self.request_id = request_id
    self.pseudonym = pseudonym
    self.consent_code = consent_code
    self.consent_version = consent_version
    self.responder_id = responder_id
    self.data_transfer_url = data_transfer_url
    self.create_date = create_date