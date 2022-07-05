from flask import request, Blueprint
from marshmallow import ValidationError
from api.constant.message_code import MessageCode
from api.exception.service_exception import ServiceException
from api.domain.data_access_response import DataAccessResponse
from api.util import exception_util, header_util, service_util
from api.schema.data_access_response_schema import DataAccessResponseSchema
from api.business_logic.data_access_response_service import DataAccessResponseService

data_access_response = Blueprint('data_access_response', __name__)

"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : data_access_response_controller.py
Purpose         : -
"""


@data_access_response.route("/submitResponse", methods=['POST'])
def submit_response():
  payload = request.get_json()

  try:
    header = header_util.build_header(request.headers)

    validated_data = DataAccessResponseSchema().load(payload)
    data_access_response = DataAccessResponse(**validated_data)

    DataAccessResponseService().submit_response(data_access_response)
    return service_util.build_status_response(MessageCode.SUCCESS.name, MessageCode.SUCCESS.value)
  except (ValidationError, ServiceException) as err:
    return exception_util.handler(err)