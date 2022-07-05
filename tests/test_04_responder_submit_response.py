import unittest
import datetime
from api.util import date_util
from api.constant.message_code import MessageCode
from tests.constant.test_constant import TestConstant
from tests.business_logic.responder_service import ResponderService

"""
Author          : Neda Peyrone
Create Date     : 29-06-2022
File            : test_05_responder_transfer_data.py
Purpose         : -
"""

class ResponderSubmitResponseTest(unittest.TestCase):
  request_id: str = None
  pseudonym: str = None
  consent_code: str = None
  consent_version: str = None

  def setUp(self):
    self.responder_service = ResponderService()

  def test_01_check_if_callback_returns(self):
    print("I:--START--:--ResponderSubmitResponseTest.test_01_check_if_callback_returns--")
    while True:
      status, body = self.responder_service.get_return_values()
      if status['code'] == MessageCode.SUCCESS.name and not (body['request_id'] is None):
        break

    self.__class__.request_id = body['request_id']
    self.__class__.pseudonym = body['pseudonym']
    self.__class__.consent_code = body['consent_code']
    self.__class__.consent_version = body['consent_version']

    print(f"O:--SUCCESS--:--ResponderSubmitResponseTest.test_01_check_if_callback_returns--:request_id/{self.__class__.request_id} \
      :pseudonym/{self.__class__.pseudonym}:consent_code/{self.__class__.consent_code} \
      :consent_version/{self.__class__.consent_version}")

  def test_02_submit_response(self):
    print("I:--START--:--ResponderSubmitResponseTest.test_02_submit_response--")
    current_date = datetime.datetime.now().astimezone().isoformat()
    current_timestamp = date_util.to_timestamp(current_date)

    payload = {}
    payload['response_id'] = f"ServiceA-{current_timestamp}"
    payload['request_id'] = self.__class__.request_id
    payload['accepted_flag'] = "Y"
    payload['accepted_message'] = "Accept a data access request."
    payload['responder_url'] = TestConstant.RESPONDER_URL
    status, body = self.responder_service.submit_response(payload)
    if status['code'] == MessageCode.SUCCESS.name:
      print(f"O:--SUCCESS--:--ResponderSubmitResponseTest.test_02_submit_response--:body/{body}")
    else:
      print(f"O:--FAIL--:--ResponderSubmitResponseTest.test_02_submit_response--:errorCode/{status['code']}:errorDesc/{status['desc']}")

