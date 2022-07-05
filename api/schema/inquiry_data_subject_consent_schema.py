from marshmallow import Schema, fields

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : inquiry_data_subject_consent_schema.py
Purpose         : -
"""


class InquiryDataSubjectConsentSchema(Schema):
  pseudonym = fields.Str(required=True)
  consent_code = fields.Str(required=True)
  consent_version = fields.Integer(required=True)
  responder_id = fields.Str(required=True)