import unittest
from api.domain.consent import Consent
from api.constant.message_code import MessageCode
from tests.constant.test_constant import TestConstant
from tests.business_logic.responder_service import ResponderService

"""
Author          : Neda Peyrone
Create Date     : 25-06-2022
File            : test_02_responder_add_data_subject_consent.py
Purpose         : -
"""

class ResponderAddDataSubjectConsentTest(unittest.TestCase):
  selected_consent: Consent = None

  def setUp(self):
    self.responder_service = ResponderService()

  def test_01_get_active_consents(self):
    print("I:--START--:--ResponderAddDataSubjectConsentTest.test_01_get_active_consents--")
    status, body = self.responder_service.list_active_consents()
    self.__class__.selected_consent = Consent(**body[0])
    if status['code'] == MessageCode.SUCCESS.name:
      print(f"O:--SUCCESS--:--ResponderAddDataSubjectConsentTest.test_01_get_active_consents--:selected_consent/{self.__class__.selected_consent}")
    else:
      print(f"O:--FAIL--:--ResponderAddDataSubjectConsentTest.test_01_get_active_consents--:errorCode/{status['code']}:errorDesc/{status['desc']}")

  def test_02_add_datasubject_consent(self):
    print("I:--START--:--ResponderAddDataSubjectConsentTest.test_02_add_datasubject_consent--")
    print(f"consent code: {self.__class__.selected_consent.consent_code}")
    print(f"consent version: {self.__class__.selected_consent.consent_version}")
    payload = {}
    payload['pseudonym'] = TestConstant.PSEUDONYM
    payload['consent_code'] = self.__class__.selected_consent.consent_code
    payload['consent_version'] = self.__class__.selected_consent.consent_version
    payload['accepted_flag'] = "Y"
    payload['responder_id'] = TestConstant.RESPONDER_ID
    payload['responder_url'] = TestConstant.RESPONDER_URL
    status, body = self.responder_service.add_data_subject_consent(payload)
    if status['code'] == MessageCode.SUCCESS.name:
      print(f"O:--SUCCESS--:--ResponderAddDataSubjectConsentTest.test_02_add_datasubject_consent--:body/{body}")
    else:
      print(f"O:--FAIL--:--ResponderAddDataSubjectConsentTest.test_02_add_datasubject_consent--:errorCode/{status['code']}:errorDesc/{status['desc']}")
