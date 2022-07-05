// SPDX-License-Identifier: MIT
pragma solidity > 0.6.1 < 0.9.0;

interface IDataAccessRequestContract {

  struct DataAccessRequest {
    string _requestId;
    string _pseudonym;
    string _consentCode;
    uint256 _consentVersion;
    address _responderId;
    uint256 _createTimestamp;
    string _dataTransferUrl;
  }

  function getDataAccessRequest(string memory _requestId) external view returns (DataAccessRequest memory);
}