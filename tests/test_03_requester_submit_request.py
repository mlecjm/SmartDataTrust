import datetime
import unittest
from api.constant.message_code import MessageCode
from api.util import date_util
from tests.constant.test_constant import TestConstant
from tests.business_logic.requester_service import RequesterService

"""
Author          : Neda Peyrone
Create Date     : 29-06-2022
File            : test_03_requester_submit_request.py
Purpose         : -
"""

class RequesterSubmitRequestTest(unittest.TestCase):
  pseudonym: str = None
  consent_code: str = None
  consent_version: str = None
  responder_id: str = None

  def setUp(self):
    self.requester_service = RequesterService()

  def test_01_check_if_callback_returns(self):
    print(f"I:--START--:--RequesterSubmitRequestTest.test_01_check_if_callback_returns--")
    while True:
      status, body = self.requester_service.get_return_values()
      if status['code'] == MessageCode.SUCCESS.name and not (body['pseudonym'] is None):
        break

    self.__class__.pseudonym = body['pseudonym']
    self.__class__.consent_code = body['consent_code']
    self.__class__.consent_version = body['consent_version']
    self.__class__.responder_id = body['responder_id']

    print(f"O:--SUCCESS--:--RequesterSubmitRequestTest.test_01_check_if_callback_returns--:pseudonym/{self.__class__.pseudonym} \
      :consent_code/{self.__class__.consent_code}:consent_version/{self.__class__.consent_version} \
      :responder_id/{self.__class__.responder_id}")

  def test_02_submit_request(self):
    print("I:--START--:--RequesterSubmitRequestTest.test_02_submit_request--")
    current_date = datetime.datetime.now().astimezone().isoformat()
    current_timestamp = date_util.to_timestamp(current_date)

    payload = {}
    payload['request_id'] = f"ServiceB-{current_timestamp}"
    payload['pseudonym'] = self.__class__.pseudonym
    payload['consent_code'] = self.__class__.consent_code
    payload['consent_version'] = self.__class__.consent_version
    payload['responder_id'] = self.__class__.responder_id
    payload['data_transfer_url'] = TestConstant.DATA_TRANSFER_URL
    status, body = self.requester_service.submit_request(payload)
    if status['code'] == MessageCode.SUCCESS.name:
      print(f"O:--SUCCESS--:--RequesterSubmitRequestTest.test_02_submit_request--:body/{body}")
    else:
      print(f"O:--FAIL--:--RequesterSubmitRequestTest.test_02_submit_request--:errorCode/{status['code']}:errorDesc/{status['desc']}")

