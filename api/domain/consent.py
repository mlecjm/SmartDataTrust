from typing import List
from api.domain.data_field import DataField

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : consent.py
Purpose         : -
"""


class Consent(object):
  id: int
  consent_code: str
  consent_detail: str
  consent_version: int
  data_retention: int
  requester_id: str
  create_date: str
  create_timestamp: int
  update_date: str
  update_timestamp: int
  requester_url: str
  active: bool
  data_fields: List[DataField]

  def __init__(
    self,
    id=None,
    consent_code=None,
    consent_detail=None, 
    consent_version=None, 
    data_retention=None, 
    requester_id=None,
    create_date=None, 
    update_date=None,
    requester_url=None,
    active=None,
    data_fields=None
  ):
    super(Consent, self).__init__()
    self.id = id
    self.consent_code = consent_code
    self.consent_detail = consent_detail
    self.consent_version = consent_version
    self.data_retention = data_retention
    self.requester_id = requester_id
    self.create_date = create_date
    self.update_date = update_date
    self.requester_url = requester_url
    self.active = active
    self.data_fields = data_fields