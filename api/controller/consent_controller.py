from flask import request, Blueprint
from api.domain.consent import Consent
from marshmallow import ValidationError
from api.constant.message_code import MessageCode
from api.schema.add_consent_schema import AddConsentSchema
from api.exception.service_exception import ServiceException
from api.business_logic.consent_service import ConsentService
from api.util import exception_util, header_util, service_util
from api.business_logic.data_field_service import DataFieldService
from api.schema.inquiry_consent_schema import InquiryConsentSchema

consent = Blueprint('consent', __name__)

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : consent_controller.py
Purpose         : -
"""


@consent.route("/addConsent", methods=['POST'])
def add_consent():
  payload = request.get_json()

  try:
    header = header_util.build_header(request.headers)

    validated_data = AddConsentSchema().load(payload)
    consent = Consent(**validated_data)

    ConsentService().add_consent(header, consent)
    DataFieldService().add_data_fields(
      header,
      consent.consent_code,
      consent.consent_version,
      consent.data_fields
    )
    return service_util.build_status_response(MessageCode.SUCCESS.name, MessageCode.SUCCESS.value)
  except (ValidationError, ServiceException) as err:
    return exception_util.handler(err)


@consent.route("/getActiveConsents", methods=['POST'])
def get_consents():
  try:
    consents = ConsentService().get_active_consents()
    data_field_service = DataFieldService()

    for idx, consent in enumerate(consents):
      data_fields = data_field_service.get_consent_data_fields(
        consent.consent_code, consent.consent_version)
      consents[idx].data_fields = data_fields

    return service_util.build_server_response(MessageCode.SUCCESS, consents)
  except (ValidationError, ServiceException) as err:
    return exception_util.handler(err)


@consent.route("/getActiveConsent", methods=['POST'])
def get_active_consent():
  payload = request.get_json()

  try:
    header = header_util.build_header(request.headers)

    validated_data = InquiryConsentSchema().load(payload)
    criteria = Consent(**validated_data)

    consent = ConsentService().get_active_consent(criteria)
    data_fields = DataFieldService().get_consent_data_fields(
    consent.consent_code, consent.consent_version)
    consent.data_fields = data_fields

    return service_util.build_server_response(MessageCode.SUCCESS, consent)
  except (ValidationError, ServiceException) as err:
    return exception_util.handler(err)
