import json
import requests
import datetime
from api.util import date_util
from api.connector.rest_client import RestClient
from tests.constant.test_constant import TestConstant
from api.exception.service_exception import ServiceException

"""
Author          : Neda Peyrone
Create Date     : 25-06-2022
File            : responder_service.py
Purpose         : -
"""


class ResponderService():

  def list_active_consents(self):
    self.session = requests.session()
    self.endpoint = f"{TestConstant.ENDPOINT}/getActiveConsents"
    self.headers = self.__build_header()
    self.payload = {}
    self.msg_action = "Get ActiveConsents"
    return self.__post()

  def add_data_subject_consent(self, payload):
    self.session = requests.session()
    self.endpoint = f"{TestConstant.ENDPOINT}/addDataSubjectConsent"
    self.headers = self.__build_header()
    self.payload = payload
    self.msg_action = "Add DataSubjectConsent"
    return self.__post()

  def submit_response(self, payload):
    self.session = requests.session()
    self.endpoint = f"{TestConstant.ENDPOINT}/submitResponse"
    self.headers = self.__build_header()
    self.payload = payload
    self.msg_action = "Submit Response"
    return self.__post()

  def transfer_data(self, payload):
    self.session = requests.session()
    self.endpoint = f"{TestConstant.ENDPOINT}/responder/receiveData"
    self.headers = self.__build_header()
    self.payload = payload
    self.msg_action = "Transfer Data"
    return self.__post()

  def get_return_values(self):
    self.session = requests.session()
    self.endpoint = f"{TestConstant.ENDPOINT}/responder/getReturnValues"
    self.headers = self.__build_header()
    self.msg_action = "Get Return Values"
    return self.__get()

  def revoke_consent(self, payload):
    self.session = requests.session()
    self.endpoint = f"{TestConstant.ENDPOINT}/revokeConsent"
    self.headers = self.__build_header()
    self.payload = payload
    self.msg_action = "Revoke Consent"
    return self.__post()

  def renew_consent(self, payload):
    self.session = requests.session()
    self.endpoint = f"{TestConstant.ENDPOINT}/renewConsent"
    self.headers = self.__build_header()
    self.payload = payload
    self.msg_action = "Renew Consent"
    return self.__post()

  def get_active_consent(self, payload):
    self.session = requests.session()
    self.endpoint = f"{TestConstant.ENDPOINT}/getActiveConsent"
    self.headers = self.__build_header()
    self.payload = payload
    self.msg_action = "Get ActiveConsent"
    return self.__post()

  def __get(self):
    try:
      print(f"I:--START--:--{self.msg_action}--:endpoint/{self.endpoint}")
      res = RestClient(self.endpoint, self.session, self.headers).get()
      json_data = res.json()
      print(f"O:--SUCCESS--:--{self.msg_action}--:status/{json_data['statusResponse']}:body/{json_data['body']}")
      return json_data['statusResponse'], json_data['body']
    except requests.exceptions.HTTPError as errh:
      print(f"O:--FAIL--:--{self.msg_action}--:errorDesc/Http Error: {errh}")
      raise ServiceException(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
      print(f"O:--FAIL--:--{self.msg_action}--:errorDesc/Error Connecting: {errc}")
      raise ServiceException(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
      print(f"O:--FAIL--:--{self.msg_action}--:errorDesc/Timeout Error: {errt}")
      raise ServiceException(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
      print(f"O:--FAIL--:--{self.msg_action}--:errorDesc/Unknown Error: {err}")
      raise ServiceException(f"Unknown Error: {err}")
    except json.JSONDecodeError as jderr:
      print(f"O:--FAIL--:--{self.msg_action}--:errorDesc/JSON Decode Error: {jderr}")
      raise ServiceException(f"JSON Decode Error: {jderr}")

  def __post(self):
    try:
      print(f"I:--START--:--{self.msg_action}--:endpoint/{self.endpoint}")
      res = RestClient(self.endpoint, self.session, self.headers, self.payload).post()
      json_data = res.json()
      print(f"O:--SUCCESS--:--{self.msg_action}--:status/{json_data['statusResponse']}:body/{json_data['body']}")
      return json_data['statusResponse'], json_data['body']
    except requests.exceptions.HTTPError as errh:
      print(f"O:--FAIL--:--{self.msg_action}--:errorDesc/Http Error: {errh}")
      raise ServiceException(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
      print(f"O:--FAIL--:--{self.msg_action}--:errorDesc/Error Connecting: {errc}")
      raise ServiceException(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
      print(f"O:--FAIL--:--{self.msg_action}--:errorDesc/Timeout Error: {errt}")
      raise ServiceException(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
      print(f"O:--FAIL--:--{self.msg_action}--:errorDesc/Unknown Error: {err}")
      raise ServiceException(f"Unknown Error: {err}")
    except json.JSONDecodeError as jderr:
      print(f"O:--FAIL--:--{self.msg_action}--:errorDesc/JSON Decode Error: {jderr}")
      raise ServiceException(f"JSON Decode Error: {jderr}")

  def __build_header(self):
    current_date = datetime.datetime.now().astimezone().isoformat()
    current_timestamp = date_util.to_timestamp(current_date)

    headers = {}
    headers['request-id'] = f"ref-no-{current_timestamp}"
    headers['caller-id'] = "Service A"
    headers['transaction-date'] = current_date
    return headers