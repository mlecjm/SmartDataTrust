import web3
import datetime
from api.util import date_util
from api.domain.header import Header
from api.domain.consent import Consent
from api.constant.message_code import MessageCode
from api.configuration.app_config import AppConfig
from api.exception.service_exception import ServiceException
from api.configuration.blockchain_config import BlockchainConfig
from api.connector.blockchain_connector import BlockchainConnector

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : consent_service.py
Purpose         : -
"""


class ConsentService:
  def __init__(self) -> None:
    self.__load_params()
    self.connector = BlockchainConnector(self.cfg)

  def __load_params(self):
    appConfig = AppConfig()
    self.cfg = BlockchainConfig(
      appConfig.params['blockchain']['address'],
      appConfig.params['api']['consent']['deployed_contract_address'],
      appConfig.params['api']['consent']['compiled_contract_path']
    )

  def add_consent(self, header: Header, consent: Consent) -> bool:
    msg_action = 'Add Consent'
    print(f'I:--START--:--{msg_action}--')
    current_date = datetime.datetime.now().astimezone().isoformat()
    current_timestamp = date_util.to_timestamp(current_date)

    validAddress = web3.Web3.toChecksumAddress(consent.requester_id)
    print(f"O:--Is the requester's address valid--:result/{validAddress}")

    try:
      is_success = self.connector.write_to_blockchain(
        'addConsent',
        consent.consent_code,
        consent.consent_detail,
        consent.consent_version,
        consent.data_retention,
        web3.Web3.toChecksumAddress(consent.requester_id),
        current_timestamp,
        0,
        consent.requester_url
      )

      # self.connector.get_event_log('consentAdded')

      print(f'O:--{"SUCCESS" if is_success else "FAIL"}--:--{msg_action}--')
      return is_success
    except (web3.exceptions.ContractLogicError, ValueError) as err:
      self.__handle_error(msg_action, err)

  def get_active_consents(self):
    msg_action = 'Get ActiveConsents'
    print(f'I:--START--:--{msg_action}--')

    try:
      results = self.connector.get_from_blockchain('getActiveConsents')
      consents = [self.__prepare_consent(r) for r in results]
      print(f'O:--SUCCESS--:--{msg_action}--:consents/{consents}')
      return consents
    except (web3.exceptions.ContractLogicError, ValueError) as err:
      self.__handle_error(msg_action, err)

  def get_active_consent(self, consent: Consent):
    msg_action = 'Get ActiveConsent'
    print(f'I:--START--:--{msg_action}--')

    try:
      result = self.connector.get_from_blockchain(
        'getConsent',
        consent.consent_code,
        consent.consent_version
      )
      consent = self.__prepare_consent(result)
      print(f'O:--SUCCESS--:--{msg_action}--')
      return consent
    except (web3.exceptions.ContractLogicError, ValueError) as err:
      self.__handle_error(msg_action, err)

  def __prepare_consent(self, obj):
    consent = Consent()
    consent.consent_code = obj[1]
    consent.consent_detail = obj[2]
    consent.consent_version = obj[3]
    consent.data_retention = obj[4]
    consent.requester_id = obj[5]
    consent.create_date = date_util.to_isoformat(obj[6])
    consent.update_date = date_util.to_isoformat(obj[7])
    consent.requester_url = obj[8]
    consent.active = obj[9]
    return consent

  def __handle_error(self, msg_action, err):
    dir(err)
    err_msg = err.args[0]['message'] if 'message' in err.args[0] else err.args[0]
    desc = MessageCode.UNKNOWN_ERROR.value if len(err.args) == 0 else err_msg.split(':')[-1].strip()
    print(f'O:--FAIL--:--{msg_action}--:errorDesc/{desc}')
    raise ServiceException(desc)