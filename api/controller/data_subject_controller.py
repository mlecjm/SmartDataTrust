from flask import request, Blueprint
from marshmallow import ValidationError
from api.constant.message_code import MessageCode
from api.exception.service_exception import ServiceException
from api.domain.data_subject_consent import DataSubjectConsent
from api.schema.revoke_consent_schema import RevokeConsentSchema
from api.util import exception_util, header_util, service_util
from api.business_logic.data_subject_service import DataSubjectService
from api.schema.add_data_subject_consent_schema import AddDataSubjectConsentSchema
from api.schema.inquiry_data_subject_consent_schema import InquiryDataSubjectConsentSchema

data_subject = Blueprint('data_subject', __name__)

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : data_subject_controller.py
Purpose         : -
"""


@data_subject.route("/addDataSubjectConsent", methods=['POST'])
def add_data_subject_consent():
  payload = request.get_json()

  try:
    print(f"I:--START--:--Add DataSubjectConsent--:pseudonym/{payload['pseudonym']}")
    header = header_util.build_header(request.headers)

    validated_data = AddDataSubjectConsentSchema().load(payload)
    data_subject_consent = DataSubjectConsent(**validated_data)

    DataSubjectService().add_data_subject_consent(header, data_subject_consent)

    return service_util.build_status_response(MessageCode.SUCCESS.name, MessageCode.SUCCESS.value)
  except (ValidationError, ServiceException) as err:
    return exception_util.handler(err)

@data_subject.route("/getDataSubjectConsent", methods=['POST'])
def get_data_subject_consent():
  payload = request.get_json()

  try:
    print(f"I:--START--:--Get DataSubjectConsent--")
    header = header_util.build_header(request.headers)

    validated_data = InquiryDataSubjectConsentSchema().load(payload)
    criteria = DataSubjectConsent(**validated_data)

    data_subject_consent = DataSubjectService().get_data_subject_consent(header, criteria)
    return service_util.build_status_response(MessageCode.SUCCESS, data_subject_consent)
  except (ValidationError, ServiceException) as err:
    return exception_util.handler(err)

@data_subject.route("/revokeConsent", methods=['POST'])
def revoke_consent():
  payload = request.get_json()

  try:
    header = header_util.build_header(request.headers)

    validated_data = RevokeConsentSchema().load(payload)
    data_subject_consent = DataSubjectConsent(**validated_data)

    DataSubjectService().revoke_consent(header, data_subject_consent)
    return service_util.build_status_response(MessageCode.SUCCESS.name, MessageCode.SUCCESS.value)
  except (ValidationError, ServiceException) as err:
    return exception_util.handler(err)

@data_subject.route("/renewConsent", methods=['POST'])
def renew_consent():
  payload = request.get_json()

  try:
    header = header_util.build_header(request.headers)

    validated_data = RevokeConsentSchema().load(payload)
    data_subject_consent = DataSubjectConsent(**validated_data)

    DataSubjectService().renew_consent(header, data_subject_consent)
    return service_util.build_status_response(MessageCode.SUCCESS.name, MessageCode.SUCCESS.value)
  except (ValidationError, ServiceException) as err:
    return exception_util.handler(err)