// SPDX-License-Identifier: MIT
pragma solidity > 0.6.1 < 0.9.0;

interface IConsentContract {

  struct Consent {
    uint256 _id;
    string _consentCode;
    string _consentDetail;
    uint256 _consentVersion;
    uint256 _dataRetention;
    address _requesterId;
    uint256 _createTimestamp;
    uint256 _updateTimestamp;
    string _requesterUrl;
    bool _active;
  }

  function getConsent(
    string memory _code, 
    uint256 _version
  ) external view returns (Consent memory consent);
}