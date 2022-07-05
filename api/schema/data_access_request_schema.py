from marshmallow import Schema, fields

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : data_access_request_schema.py
Purpose         : -
"""

class DataAccessRequestSchema(Schema):
  request_id = fields.Str(required=True)
  pseudonym = fields.Str(required=True)
  consent_code = fields.Str(required=True)
  consent_version = fields.Integer(required=True)
  responder_id = fields.Str(required=True)
  data_transfer_url = fields.Str(required=True)
