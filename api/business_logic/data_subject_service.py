import web3
import datetime
from api.util import date_util
from api.domain.header import Header
from api.constant.message_code import MessageCode
from api.configuration.app_config import AppConfig
from api.exception.service_exception import ServiceException
from api.domain.data_subject_consent import DataSubjectConsent
from api.configuration.blockchain_config import BlockchainConfig
from api.connector.blockchain_connector import BlockchainConnector

"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : data_subject_service.py
Purpose         : -
"""


class DataSubjectService():
  def __init__(self) -> None:
    self.__load_params()
    self.connector = BlockchainConnector(self.cfg)

  def __load_params(self):
    appConfig = AppConfig()
    self.cfg = BlockchainConfig(
      appConfig.params['blockchain']['address'],
      appConfig.params['api']['data_subject_consent']['deployed_contract_address'],
      appConfig.params['api']['data_subject_consent']['compiled_contract_path']
    )

  def add_data_subject_consent(self, header: Header, dataSubjectConsent: DataSubjectConsent) -> bool:
    msg_action = "Add DataSubjectConsent"
    print(f'I:--START--:--{msg_action}--')

    current_date = datetime.datetime.now().astimezone().isoformat()
    current_timestamp = date_util.to_timestamp(current_date)

    try:
      is_success = self.connector.write_to_blockchain(
        'addDataSubjectConsent',
        dataSubjectConsent.pseudonym,
        dataSubjectConsent.consent_code,
        dataSubjectConsent.consent_version,
        web3.Web3.toChecksumAddress(dataSubjectConsent.responder_id),
        dataSubjectConsent.accepted_flag,
        current_timestamp,
        "",
        0,
        dataSubjectConsent.responder_url
      )

      print(f'O:--{"SUCCESS" if is_success else "FAIL"}--:--{msg_action}--')
      return is_success
    except (web3.exceptions.ContractLogicError, ValueError) as err:
      self.__handle_error(msg_action, err)

  def get_data_subject_consent(self, header: Header, dataSubjectConsent: DataSubjectConsent):
    msg_action = 'Get DataSubjectConsent'
    print(f'I:--START--:--{msg_action}--')

    try:
      result = self.connector.get_from_blockchain(
        'getDataSubjectConsent',
        dataSubjectConsent.pseudonym,
        dataSubjectConsent.consent_code,
        dataSubjectConsent.consent_version,
        web3.Web3.toChecksumAddress(dataSubjectConsent.responder_id)
      )
      dataSubjectConsent = DataSubjectConsent(*result)
      print(f'O:--SUCCESS--:--{msg_action}--')
      return dataSubjectConsent
    except (web3.exceptions.ContractLogicError, ValueError) as err:
      self.__handle_error(msg_action, err)

  def revoke_consent(self, header: Header, dataSubjectConsent: DataSubjectConsent):
    msg_action = 'Revoke Consent'
    print(f'I:--START--:--{msg_action}--')

    current_date = datetime.datetime.now().astimezone().isoformat()
    current_timestamp = date_util.to_timestamp(current_date)

    try:
      is_success = self.connector.write_to_blockchain(
        'revokeConsent',
        dataSubjectConsent.pseudonym,
        dataSubjectConsent.consent_code,
        dataSubjectConsent.consent_version,
        web3.Web3.toChecksumAddress(dataSubjectConsent.responder_id),
        current_timestamp
      )
      print(f'O:--{"SUCCESS" if is_success else "FAIL"}--:--{msg_action}--')
      return is_success
    except (web3.exceptions.ContractLogicError, ValueError) as err:
      self.__handle_error(msg_action, err)

  def renew_consent(self, header: Header, dataSubjectConsent: DataSubjectConsent):
    msg_action = "Renew Consent"
    print(f'I:--START--:--{msg_action}--')

    current_date = datetime.datetime.now().astimezone().isoformat()
    current_timestamp = date_util.to_timestamp(current_date)

    try:
      is_success = self.connector.write_to_blockchain(
        'renewConsent',
        dataSubjectConsent.pseudonym,
        dataSubjectConsent.consent_code,
        dataSubjectConsent.consent_version,
        dataSubjectConsent.responder_id,
        current_timestamp
      )
      print(f'O:--{"SUCCESS" if is_success else "FAIL"}--:--{msg_action}--')
      return is_success
    except (web3.exceptions.ContractLogicError, ValueError) as err:
      self.__handle_error(msg_action, err)

  def __handle_error(self, msg_action, err):
    dir(err)
    err_msg = err.args[0]['message'] if 'message' in err.args[0] else err.args[0]
    desc = MessageCode.UNKNOWN_ERROR.value if len(err.args) == 0 else err_msg.split(':')[-1].strip()
    print(f'O:--FAIL--:--{msg_action}--:errorDesc/{desc}')
    raise ServiceException(desc)