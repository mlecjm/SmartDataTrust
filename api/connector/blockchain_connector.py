import json
from typing import Optional
from web3 import Web3, HTTPProvider
from api.configuration.blockchain_config import BlockchainConfig

"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : blockchain_connector.py
Purpose         : -
"""


class BlockchainConnector:

  def __init__(self, config: Optional[BlockchainConfig]) -> None:
    self.config = config
    self.is_connected = False
    self.w3 = None
    self.contract = None
    self.__setup()

  def __is_connected(self) -> None:
    """
    Connect to blockchain
    :returns: connection state
    """
    w3 = Web3(HTTPProvider(self.config.blockchain_address))
    if w3.isConnected():
      self.is_connected = True
      self.w3 = w3
      return True
    return False

  def __setup_contract(self) -> None:
    """
    setup contract and account if connected
    :returns: None
    """
    if self.is_connected:
      self.w3.eth.defaultAccount = self.w3.toChecksumAddress(self.w3.eth.accounts[0])

      with open(self.config.compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']

      self.contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(self.config.deployed_contract_address), abi=contract_abi)

  def __setup(self) -> None:
    """
    setup connection and contract
    :returns: None
    """
    self.__is_connected()
    if self.is_connected:
      self.__setup_contract()

  def get_from_blockchain(self, func_name, *args):
    """ 
    Read data from blockchain
    :param data: any kind of data due to smart contract function which will be called
    :returns: data read from blockchain
    """
    if self.is_connected:
      return self.contract.functions[func_name](*args).call()

  def write_to_blockchain(self, func_name, *args) -> bool:
    """
    Write data to blockchain
    :param data: any kind of data due to smart contract function which will be called
    :returns: transaction successfull state
    """
    if self.is_connected:
      tx_hash = self.contract.functions[func_name](*args).transact()
      self.tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

      print(f"tx_receipt: {self.tx_receipt}")
      print(f"Transaction receipt mined : {dict(self.tx_receipt)}")
      print(f"Was transaction successful? : {self.tx_receipt['status']}")

      tx_data = self.w3.eth.getTransaction(self.tx_receipt['transactionHash'])
      func_obj, func_params = self.contract.decode_function_input(tx_data.input)
      print(f"func_obj: {func_obj} | func_params: {func_params}")
    return self.tx_receipt['status'] == 1

  def get_event_log(self, func_name):
    if self.is_connected:
      result = self.contract.events[func_name]().processReceipt(self.tx_receipt)
      print(f"O:--Get Event Log--:result/{result[0]}")

