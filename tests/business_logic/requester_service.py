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
File            : requester_service.py
Purpose         : -
"""


class RequesterService():

  def add_consent(self, payload):
    self.session = requests.session()
    self.endpoint = f"{TestConstant.ENDPOINT}/addConsent"
    self.headers = self.__build_header()
    self.payload = payload
    self.msg_action = "Add Consent"
    return self.__post()

  def submit_request(self, payload):
    self.session = requests.session()
    self.endpoint = f"{TestConstant.ENDPOINT}/submitRequest"
    self.headers = self.__build_header()
    self.payload = payload
    self.msg_action = "Submit Request"
    return self.__post()

  def get_return_values(self):
    self.session = requests.session()
    self.endpoint = f"{TestConstant.ENDPOINT}/requester/getReturnValues"
    self.headers = self.__build_header()
    self.msg_action = "Get Return Values"
    return self.__get()

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
    headers['caller-id'] = "Service B"
    headers['transaction-date'] = current_date
    return headers