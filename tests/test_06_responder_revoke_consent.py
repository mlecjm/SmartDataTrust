import unittest
from api.constant.message_code import MessageCode
from tests.constant.test_constant import TestConstant
from tests.business_logic.responder_service import ResponderService

"""
Author          : Neda Peyrone
Create Date     : 30-06-2022
File            : test_06_responder_revoke_consent.py
Purpose         : -
"""

class ResponderRevokeConsentTest(unittest.TestCase):
  
  def setUp(self):
    self.responder_service = ResponderService()

  def test_01_revoke_consent(self):
    print("I:--START--:--ResponderRevokeConsentTest.test_01_revoke_consent--")
    payload = {}
    payload['pseudonym'] = TestConstant.PSEUDONYM
    payload['consent_code'] = TestConstant.CONSENT_CODE
    payload['consent_version'] = TestConstant.CONSENT_VERSION
    payload['responder_id'] = TestConstant.RESPONDER_ID
    status, body = self.responder_service.revoke_consent(payload)
    if status['code'] == MessageCode.SUCCESS.name:
      print(f"O:--SUCCESS--:--ResponderRevokeConsentTest.test_01_revoke_consent--:body/{body}")
    else:
      print(f"O:--FAIL--:--ResponderRevokeConsentTest.test_01_revoke_consent--:errorCode/{status['code']}:errorDesc/{status['desc']}")
