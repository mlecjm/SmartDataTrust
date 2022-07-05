import json
from pathlib import Path
from urllib.parse import parse_qs
from flask import request, Blueprint
from tests.domain.parameter import Parameter
from api.constant.message_code import MessageCode
from api.util import encryption_util, service_util

responder = Blueprint('responder', __name__, url_prefix='/responder')

"""
Author          : Neda Peyrone
Create Date     : 25-06-2021
File            : responder_controller.py
Purpose         : -
"""


@responder.route("/receiveCallback", methods=['POST'])
def receive_callback():
  print(f"I:--START--:--DataTransfer Callback--")
  body = request.stream.read().decode("utf-8")
  # qs = json.loads(body)
  qs = parse_qs(body)

  parameter = Parameter()

  if not ('transfer_url' in qs):
    parameter.request_id = qs['request_id'][0]
    parameter.pseudonym = qs['pseudonym'][0]
    parameter.consent_code = qs['consent_code'][0]
    parameter.consent_version = qs['consent_version'][0]

    print(f"I:--START--:--Receive Callback--:request_id/{parameter.request_id} \
      :pseudonym/{parameter.pseudonym}:consent_code/{parameter.consent_code} \
      :consent_version/{parameter.consent_version}")
  else:
    parameter.response_id = qs['response_id'][0]
    parameter.data_transfer_url = qs['transfer_url'][0]

    print(f"O:--SUCCESS--:--DataTransfer Callback--:response_id/{parameter.responder_id} \
      :data_transfer_url/{parameter.data_transfer_url}")

  return service_util.build_status_response(MessageCode.SUCCESS.name, MessageCode.SUCCESS.value)

@responder.route("/receiveData", methods=['POST'])
def receive_data():
  print("I:--START--:--Receive Data--")
  body = request.stream.read().decode("utf-8")
  qs = json.loads(body)
  encrypted_data = qs['encrypted_data']

  path = f"{Path().absolute()}/tests/keys"
  json_string = encryption_util.decrypt(f"{path}/private_key.pem", encrypted_data)
  personal_data = json.loads(json_string)

  print(f"O:--SUCCESS--:--Receive Data--:personal_data/{personal_data}")
  return service_util.build_status_response(MessageCode.SUCCESS.name, MessageCode.SUCCESS.value)

@responder.route("/getReturnValues", methods=['GET'])
def get_return_values():
  parameter = Parameter()
  values = {}
  values['request_id'] = parameter.request_id
  values['pseudonym'] = parameter.pseudonym
  values['consent_code'] = parameter.consent_code
  values['consent_version'] = parameter.consent_version
  if hasattr(parameter, 'response_id'):
    values['response_id'] = parameter.response_id
  if hasattr(parameter, 'data_transfer_url'):
    values['data_transfer_url'] = parameter.data_transfer_url  
  return service_util.build_server_response(MessageCode.SUCCESS, values)
