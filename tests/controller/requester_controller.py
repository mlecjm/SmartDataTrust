# import json
from urllib.parse import parse_qs
from api.util import service_util
from flask import request, Blueprint
from tests.domain.parameter import Parameter
from api.constant.message_code import MessageCode

requester = Blueprint('requester', __name__, url_prefix='/requester')

"""
Author          : Neda Peyrone
Create Date     : 25-06-2021
File            : requester_controller.py
Purpose         : -
"""


@requester.route("/receiveCallback", methods=['POST'])
def receive_callback():
  print("I:--START--:--Receive Callback--")
  body = request.stream.read().decode("utf-8")
  # qs = json.loads(body)
  qs = parse_qs(body)

  parameter = Parameter()
  parameter.pseudonym = qs['pseudonym'][0]
  parameter.consent_code = qs['consent_code'][0]
  parameter.consent_version = qs['consent_version'][0]
  parameter.responder_id = qs['responder_id'][0]

  print(f"O:--SUCCESS--:--Receive Callback--:pseudonym/{parameter.pseudonym} \
    :consent_code/{parameter.consent_code}:consent_version/{parameter.responder_id} \
    :responder_id/{parameter.consent_version}")
  
  return service_util.build_status_response(MessageCode.SUCCESS.name, MessageCode.SUCCESS.value)

@requester.route("/getReturnValues", methods=['GET'])
def get_return_values():
  parameter = Parameter()
  values = {}
  values['pseudonym'] = parameter.pseudonym
  values['consent_code'] = parameter.consent_code
  values['consent_version'] = parameter.consent_version
  values['responder_id'] = parameter.responder_id
  return service_util.build_server_response(MessageCode.SUCCESS, values)