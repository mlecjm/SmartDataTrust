// SPDX-License-Identifier: MIT
pragma solidity > 0.6.1 < 0.9.0;

interface IDataFieldContract {

  struct DataField {
    uint256 _id;
    string _fieldName;
    string _consentCode;
    uint256 _consentVersion;
  }
}