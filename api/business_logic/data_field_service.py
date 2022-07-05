import web3
from api.domain.header import Header
from api.domain.data_field import DataField
from api.constant.message_code import MessageCode
from api.configuration.app_config import AppConfig
from api.exception.service_exception import ServiceException
from api.configuration.blockchain_config import BlockchainConfig
from api.connector.blockchain_connector import BlockchainConnector

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : data_field_service.py
Purpose         : -
"""

class DataFieldService:
  def __init__(self) -> None:
    self.__load_params()
    self.connector = BlockchainConnector(self.cfg)

  def __load_params(self):
    appConfig = AppConfig()
    self.cfg = BlockchainConfig(
      appConfig.params['blockchain']['address'],
      appConfig.params['api']['data_field']['deployed_contract_address'],
      appConfig.params['api']['data_field']['compiled_contract_path']
    )

  def add_data_fields(self, header: Header, consent_code: str, consent_version: int, data_fields: any) -> bool:
    msg_action = 'Add DataFields'
    print(f'I:--START--:--{msg_action}--:data_fields/{data_fields}')

    try:
      for data_field in data_fields:
        self.connector.write_to_blockchain(
          'addDataField',
          data_field['field_name'],
          consent_code,
          consent_version
        )

      print(f'O:--SUCCESS--:--{msg_action}--')
      return True
    except (web3.exceptions.ContractLogicError, ValueError) as err:
      self.__handle_error(msg_action, err)

  def get_consent_data_fields(self, consent_code, consent_version):
    msg_action = 'Get ConsentDataFields'
    print(f'I:--START--:--{msg_action}--')

    try:
      results = self.connector.get_from_blockchain(
        'getConsentDataFields',
        consent_code,
        consent_version
      )
      data_fields = [self.__prepare_data_field(r) for r in results]
      print(f'O:--SUCCESS--:--{msg_action}--:data_fields/{data_fields}')
      return data_fields
    except (web3.exceptions.ContractLogicError, ValueError) as err:
      self.__handle_error(msg_action, err)

  def __prepare_data_field(self, obj):
    data_field = DataField()
    data_field.field_name = obj[1]
    data_field.consent_code = obj[2]
    data_field.consent_version = obj[3]
    return data_field

  def __handle_error(self, msg_action, err):
    dir(err)
    err_msg = err.args[0]['message'] if 'message' in err.args[0] else err.args[0]
    desc = MessageCode.UNKNOWN_ERROR.value if len(err.args) == 0 else err_msg.split(':')[-1].strip()
    print(f'O:--FAIL--:--{msg_action}--:errorDesc/{desc}')
    raise ServiceException(desc)