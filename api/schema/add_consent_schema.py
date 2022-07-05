from marshmallow import Schema, fields
from api.schema.add_data_field_schema import AddDataFieldSchema

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : add_consent_schema.py
Purpose         : -
"""


class AddConsentSchema(Schema):
  consent_code = fields.Str(required=True)
  consent_detail = fields.Str(required=True)
  consent_version = fields.Integer(required=True)
  data_retention = fields.Integer(required=True)
  requester_id = fields.Str(required=True)
  requester_url = fields.Str(required=True)
  data_fields = fields.List(
    fields.Nested(AddDataFieldSchema),
    required=True
  )
