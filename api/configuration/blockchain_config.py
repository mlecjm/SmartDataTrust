"""
Author          : Neda Peyrone
Create Date     : 05-09-2021
File            : blockchain_config.py
Purpose         : This python file is used to contains the necessary parameters for connecting to blockchain smart contract
"""


class BlockchainConfig:
  blockchain_address: str
  deployed_contract_address: str
  compiled_contract_path: str

  def __init__(self, blockchain_address, contract_address, contract_path) -> None:
    self.blockchain_address = blockchain_address
    self.deployed_contract_address = contract_address
    self.compiled_contract_path = contract_path

  def __repr__(self):
    return "<BlockchainConfig(name={self.name!r})>".format(self=self)