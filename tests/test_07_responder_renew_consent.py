import unittest
from api.constant.message_code import MessageCode
from tests.business_logic.responder_service import ResponderService
from tests.constant.test_constant import TestConstant

"""
Author          : Neda Peyrone
Create Date     : 30-06-2022
File            : test_07_responder_renew_consent.py
Purpose         : -
"""

class ResponderRenewConsentTest(unittest.TestCase):

  def setUp(self):
    self.responder_service = ResponderService()

  def test_01_renew_consent(self):
    print("I:--START--:--ResponderRenewConsentTest.test_01_renew_consent--")
    payload = {}
    payload['pseudonym'] = TestConstant.PSEUDONYM
    payload['consent_code'] = TestConstant.CONSENT_CODE
    payload['consent_version'] = TestConstant.CONSENT_VERSION
    payload['responder_id'] = TestConstant.RESPONDER_ID
    status, body = self.responder_service.renew_consent(payload)
    if status['code'] == MessageCode.SUCCESS.name:
      print(f"O:--SUCCESS--:--ResponderRenewConsentTest.test_01_renew_consent--:body/{body}")
    else:
      print(f"O:--FAIL--:--ResponderRenewConsentTest.test_01_renew_consent--:errorCode/{status['code']}:errorDesc/{status['desc']}")

