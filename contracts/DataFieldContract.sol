// SPDX-License-Identifier: MIT
pragma solidity > 0.6.1 < 0.9.0;

import "./ConsentContract.sol";
import "./IDataFieldContract.sol";

/// @author Neda Peyrone
/// @dev This solidity is used to manage data field into a blockchain.
contract DataFieldContract is IDataFieldContract {
  uint256 public dataFieldCount = 0;
  mapping(string => mapping(uint256 => mapping(string => bool))) dataFieldExists;
  mapping(uint256 => DataField) public dataFields;
  mapping(string => mapping(uint256 => DataField[])) public consentDataFields;

  event LogAddedDataField(uint256 _idx, string _consentCode, uint256 _consentVersion, string _fieldName);

  IConsentContract consentContract;

  constructor(address _consentContractAddress) {
    consentContract = ConsentContract(_consentContractAddress);
  }

  function addDataField(
    string memory _fieldName,
    string memory _consentCode,
    uint256 _consentVersion
  ) public {
    require(!dataFieldExists[_consentCode][_consentVersion][_fieldName], "Error: Duplicate Field name.");
    uint256 _candidateId = dataFieldCount+1;
    dataFields[dataFieldCount] = DataField(
      dataFieldCount+1,
      _fieldName,
      _consentCode,
      _consentVersion
    );
    dataFieldExists[_consentCode][_consentVersion][_fieldName] = true;
    consentDataFields[_consentCode][_consentVersion].push(dataFields[dataFieldCount]);
    incrementCount();
    emit LogAddedDataField(_candidateId, _consentCode, _consentVersion, _fieldName);
  }

  function incrementCount() internal {
    dataFieldCount += 1;
  }

  function getConsentDataFields(
    string memory _consentCode,
    uint256 _consentVersion
  ) public view returns (DataField[] memory) {
    IConsentContract.Consent memory consent = consentContract.getConsent(_consentCode, _consentVersion);
    DataField[] storage dataFieldArray = consentDataFields[consent._consentCode][consent._consentVersion];
    return dataFieldArray;
  }
}