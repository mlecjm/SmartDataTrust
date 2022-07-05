from marshmallow import Schema, fields

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : add_data_field_schema.py
Purpose         : -
"""


class AddDataFieldSchema(Schema):
  field_name = fields.Str(required=True)
