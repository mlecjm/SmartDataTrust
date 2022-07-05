from marshmallow import Schema, fields

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : add_data_subject_consent_schema.py
Purpose         : -
"""


class AddDataSubjectConsentSchema(Schema):
  pseudonym = fields.Str(required=True)
  consent_code = fields.Str(required=True)
  consent_version = fields.Integer(required=True)
  accepted_flag = fields.Str(required=True)
  responder_id = fields.Str(required=True)
  responder_url = fields.Str(required=True)