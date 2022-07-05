from api.util import json_util
from api.constant.message_code import MessageCode
from api.domain.status_response import StatusResponse
from api.domain.server_response import ServerReponse

"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : service_util.py
Purpose         : -
"""


def build_status_response(respCode: str, respMsg: str):
  status_response = StatusResponse(respCode, respMsg)
  res = ServerReponse(status_response, None)
  return json_util.to_json(res), 200,  {'Content-Type': 'application/json; charset=utf-8'}


def build_server_response(msgCode: MessageCode, body: any):
  status_response = StatusResponse(msgCode.name, msgCode.value)
  res = ServerReponse(status_response, body)
  return json_util.to_json(res), 200, {'Content-Type': 'application/json; charset=utf-8'}
