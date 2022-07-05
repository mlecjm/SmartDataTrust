// SPDX-License-Identifier: MIT
pragma solidity > 0.6.1 < 0.9.0;

interface IDataSubjectConsentContract {

  struct DataSubjectConsent {
    uint256 _id;
    string _pseudonym;
    string _consentCode;
    uint256 _consentVersion;
    address _responderId;
    string _acceptedFlag;
    uint256 _createTimestamp;
    string _withdrawnFlag;
    uint256 _withdrawnTimestamp;
    string _responderUrl;
  }

  function isConsentValid(
    string memory _pseudonym, 
    string memory _consentCode, 
    uint256 _consentVersion,
    address _responderId
  ) external view returns(bool);

  function getDataSubjectConsent(
    string memory _pseudonym, 
    string memory _consentCode, 
    uint256 _consentVersion,
    address _responderId
  ) external view returns (DataSubjectConsent memory);
}