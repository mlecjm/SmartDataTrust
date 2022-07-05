from flask.wrappers import Request
from api.domain.header import Header
from api.schema.header_schema import HeaderSchema

"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : header_util.py
Purpose         : -
"""


def build_header(request: Request):
  reqHeader = {}
  if "request-id" in request:
    reqHeader['request_id'] = request['request-id']
  if "caller-id" in request:
    reqHeader['caller_id'] = request['caller-id']
  if "transaction-date" in request:
    reqHeader['transaction_date'] = request['transaction-date']

  headerSchema = HeaderSchema().load(reqHeader)
  header = Header(**headerSchema)
  return header