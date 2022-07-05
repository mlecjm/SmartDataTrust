from marshmallow import Schema, fields

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : inquiry_consent_schema.py
Purpose         : -
"""


class InquiryConsentSchema(Schema):
  consent_code = fields.Str(required=True)
  consent_version = fields.Integer(required=True)
