from api.util import service_util
from marshmallow import ValidationError
from api.constant.message_code import MessageCode
from api.exception.service_exception import ServiceException

"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : exception_util.py
Purpose         : -
"""


def handler(err):
  result = __handler_error(err)
  return service_util.build_status_response(result[0], result[1])

def __handler_error(err):
  if isinstance(err, ValidationError):
    return (MessageCode.ERROR_INVALID_PARAM.name, err.messages)
  elif isinstance(err, ServiceException):
    return (MessageCode.ERROR_CONTRACT_LOGIC.name, err.msg)
  return (MessageCode.UNKNOWN_ERROR.name, MessageCode.UNKNOWN_ERROR.value)