from marshmallow import Schema, fields

"""
Author          : Neda Peyrone
Create Date     : 30-06-2022
File            : revoke_consent_schema.py
Purpose         : -
"""


class RevokeConsentSchema(Schema):
  pseudonym = fields.Str(required=True)
  consent_code = fields.Str(required=True)
  consent_version = fields.Integer(required=True)
  responder_id = fields.Str(required=True)