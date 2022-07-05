import unittest
from api.constant.message_code import MessageCode
from tests.constant.test_constant import TestConstant
from tests.business_logic.requester_service import RequesterService

"""
Author          : Neda Peyrone
Create Date     : 25-06-2022
File            : test_01_requester_add_consent.py
Purpose         : -
"""


class RequesterAddConsentTest(unittest.TestCase):

  def setUp(self):
    self.requester_service = RequesterService()

  def test_01_add_consent(self):
    print(f"I:--START--:--RequesterAddConsentTest.test_01_add_consent--")
    payload = {}
    payload['consent_code'] = TestConstant.CONSENT_CODE
    payload['consent_detail'] = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy \
      text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five \
      centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset \
      sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. Why do \
      we use it? It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of \
      using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like \
      readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem \
      ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose \
      (injected humour and the like)."
    payload['consent_version'] = TestConstant.CONSENT_VERSION
    payload['data_retention'] = TestConstant.DATA_RETENTION
    payload['requester_id'] = TestConstant.REQUESTER_ID
    payload['requester_url'] = TestConstant.REQUESTER_URL
    payload['data_fields'] = [
      { "field_name": "Name" },
      { "field_name": "BirthDate" },
      { "field_name": "BirthDefects" }
    ]
    status, body = self.requester_service.add_consent(payload)
    if status['code'] == MessageCode.SUCCESS.name:
      print(f"O:--SUCCESS--:--RequesterAddConsentTest.test_01_add_consent--:body/{body}")
    else:
      print(f"O:--FAIL--:--RequesterAddConsentTest.test_01_add_consent--:errorCode/{status['code']}:errorDesc/{status['desc']}")
