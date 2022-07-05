"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : data_field.py
Purpose         : -
"""

class DataField(object):
  id: int
  field_name: str
  consent_code: str
  consent_version: int

  def __init__(
    self,
    id=None,
    field_name=None,
    consent_code=None,
    consent_version=None
  ):
    super(DataField, self).__init__()
    self.id = id
    self.field_name = field_name
    self.consent_code = consent_code
    self.consent_version = consent_version