from flask import request, Blueprint
from marshmallow import ValidationError
from api.constant.message_code import MessageCode
from api.domain.data_access_request import DataAccessRequest
from api.exception.service_exception import ServiceException
from api.util import exception_util, header_util, service_util
from api.schema.data_access_request_schema import DataAccessRequestSchema
from api.business_logic.data_access_request_service import DataAccessRequestService

data_access_request = Blueprint('data_access_request', __name__)

"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : data_access_request_controller.py
Purpose         : -
"""


@data_access_request.route("/submitRequest", methods=['POST'])
def submit_request():
  payload = request.get_json()

  try:
    header = header_util.build_header(request.headers)

    validated_data = DataAccessRequestSchema().load(payload)
    data_access_request = DataAccessRequest(**validated_data)

    DataAccessRequestService().submit_request(data_access_request)
    return service_util.build_status_response(MessageCode.SUCCESS.name, MessageCode.SUCCESS.value)
  except (ValidationError, ServiceException) as err:
    return exception_util.handler(err)
