import web3
import datetime
from api.util import date_util
from api.constant.message_code import MessageCode
from api.configuration.app_config import AppConfig
from api.exception.service_exception import ServiceException
from api.domain.data_access_request import DataAccessRequest
from api.configuration.blockchain_config import BlockchainConfig
from api.connector.blockchain_connector import BlockchainConnector

"""
Author          : Neda Peyrone
Create Date     : 12-09-2021
File            : data_access_request_service.py
Purpose         : -
"""


class DataAccessRequestService():
  def __init__(self) -> None:
    self.__load_params()
    self.connector = BlockchainConnector(self.cfg)

  def __load_params(self):
    appConfig = AppConfig()
    self.cfg = BlockchainConfig(
      appConfig.params['blockchain']['address'],
      appConfig.params['api']['data_access_request']['deployed_contract_address'],
      appConfig.params['api']['data_access_request']['compiled_contract_path']
    )

  def submit_request(self, dataAccessRequest: DataAccessRequest):
    msg_action = 'Submit Request'
    request_id = dataAccessRequest.request_id
    print(f'I:--START--:--{msg_action}--:request_id/{request_id}')

    current_date = datetime.datetime.now().astimezone().isoformat()
    create_timestamp = date_util.to_timestamp(current_date)

    try:
      is_success = self.connector.write_to_blockchain(
        'submitRequest',
        request_id,
        dataAccessRequest.pseudonym,
        dataAccessRequest.consent_code,
        dataAccessRequest.consent_version,
        web3.Web3.toChecksumAddress(dataAccessRequest.responder_id),
        create_timestamp,
        dataAccessRequest.data_transfer_url
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