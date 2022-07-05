from marshmallow import Schema, fields

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : header_schema.py
Purpose         : -
"""

class HeaderSchema(Schema):
  request_id = fields.Str(required=False)
  caller_id = fields.Str(required=False)
  transaction_date = fields.Str(required=False)
