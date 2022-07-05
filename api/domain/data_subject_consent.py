"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : data_subject_consent.py
Purpose         : -
"""


class DataSubjectConsent(object):
  id: int
  pseudonym: str
  consent_code: str
  consent_version: int
  responder_id: str
  accepted_flag: str
  create_date: str
  withdrawn_flag: str
  withdrawn_date: str
  responder_url: str

  def __init__(
    self,
    id=None,
    pseudonym=None,
    consent_code=None,
    consent_version=None,
    responder_id=None,
    accepted_flag=None,
    create_date=None,
    withdrawn_flag=None,
    withdrawn_date=None,
    responder_url=None
  ):
    super(DataSubjectConsent, self).__init__()
    self.id = id
    self.pseudonym = pseudonym
    self.consent_code = consent_code
    self.consent_version = consent_version
    self.responder_id = responder_id
    self.accepted_flag = accepted_flag
    self.create_date = create_date
    self.withdrawn_flag = withdrawn_flag
    self.withdrawn_date = withdrawn_date
    self.responder_url = responder_url
