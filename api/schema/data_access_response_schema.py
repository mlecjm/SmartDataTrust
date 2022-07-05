from marshmallow import Schema, fields

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : data_access_response_schema.py
Purpose         : -
"""

class DataAccessResponseSchema(Schema):
  response_id = fields.Str(required=True)
  request_id = fields.Str(required=True)
  accepted_flag = fields.Str(required=True)
  accepted_message = fields.Str(required=True)
  responder_url = fields.Str(required=True)
