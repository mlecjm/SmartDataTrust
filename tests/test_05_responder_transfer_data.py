import json
import unittest
from pathlib import Path
from api.constant.message_code import MessageCode
from api.util import encryption_util
from tests.business_logic.responder_service import ResponderService
from tests.constant.test_constant import TestConstant

"""
Author          : Neda Peyrone
Create Date     : 30-06-2022
File            : test_05_responder_transfer_data.py
Purpose         : -
"""

class ResponderTransferDataTest(unittest.TestCase):
  request_id: str = None
  pseudonym: str = None
  consent_code: str = None
  consent_version: str = None
  response_id: str = None
  data_transfer_url: str = None
  
  def setUp(self):
    self.responder_service = ResponderService()

  def test_01_check_if_callback_returns(self):
    print("I:--START--:--ResponderTransferDataTest.test_01_check_if_callback_returns--")
    while True:
      status, body = self.responder_service.get_return_values()
      if status['code'] == MessageCode.SUCCESS.name and not (body['data_transfer_url'] is None):
        break

    self.__class__.request_id = body['request_id']
    self.__class__.pseudonym = body['pseudonym']
    self.__class__.consent_code = body['consent_code']
    self.__class__.consent_version = body['consent_version']
    self.__class__.response_id = body['response_id']
    self.__class__.data_transfer_url = body['data_transfer_url']

    print(f"O:--SUCCESS--:--ResponderTransferDataTest.test_01_check_if_callback_returns--:request_id/{self.__class__.request_id} \
      :pseudonym/{self.__class__.pseudonym}:consent_code/{self.__class__.consent_code} \
      :consent_version/{self.__class__.consent_version}:response_id/{self.__class__.response_id} \
      :data_transfer_url/{self.__class__.data_transfer_url}")

  def test_02_transfer_data(self):
    print("I:--START--:--ResponderTransferDataTest.test_02_transfer_data--")

    payload = {}
    payload['consent_code'] = self.__class__.consent_code
    payload['consent_version'] = self.__class__.consent_version
    status, body = self.responder_service.get_active_consent(payload)
    if status['code'] == MessageCode.SUCCESS.name:
      self.data_fields = body['data_fields']

    payload = {}
    payload['request_id'] = self.__class__.request_id
    payload['pseudonym'] = self.__class__.pseudonym

    result = {}
    personal_data = TestConstant.PERSONAL_DATA[TestConstant.PSEUDONYM]
    for field in self.data_fields:
      result[field['field_name']] = personal_data[field['field_name']]

    path = f"{Path().absolute()}/tests/keys"
    payload["encrypted_data"] = str(encryption_util.encrypt(f"{path}/public_key.pem", json.dumps(result)), encoding="UTF-8")
    status, body = self.responder_service.transfer_data(payload)
    if status['code'] == MessageCode.SUCCESS.name:
      print(f"O:--SUCCESS--:--ResponderTransferDataTest.test_02_transfer_data--:body/{body}")
    else:
      print(f"O:--FAIL--:--ResponderTransferDataTest.test_02_transfer_data--:errorCode/{status['code']}:errorDesc/{status['desc']}")
