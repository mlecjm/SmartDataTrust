// SPDX-License-Identifier: MIT
pragma solidity > 0.6.1 < 0.9.0;

import "./IConsentContract.sol";

/// @author Neda Peyrone
/// @dev This solidity is used to manage consent into a blockchain.
contract ConsentContract is IConsentContract {
  uint256 public consentCount = 0;
  mapping(uint256 => Consent) public consents;
  mapping(string => mapping(uint256 => Entry)) public consentExists;

  event LogAddedConsent(uint256 _idx, string _code, string _detail, uint256 _version, uint256 _retention, 
    address indexed _requesterId, uint256 _createTimestamp, string _requesterUrl);
  event LogInactivatedConsent(uint256 _idx, string _code, uint256 _version, uint256 _updateTimestamp);

  address owner;

  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }

  struct Entry {
    uint256 _idx;
    bool _active;
    bool _exists;
  }

  function addConsent(
    string memory _code,
    string memory _detail,
    uint256 _version,
    uint256 _retention,
    address _requesterId,
    uint256 _createTimestamp,
    uint256 _updateTimestamp,
    string memory _requesterUrl
  ) public {
    require(!consentExists[_code][_version]._exists, "Error: Duplicate Consent Code.");
    uint256 _candidateId = consentCount+1;
    consents[consentCount] = Consent(
      _candidateId,
      _code,
      _detail,
      _version,
      _retention,
      _requesterId,
      _createTimestamp,
      _updateTimestamp,
      _requesterUrl,
      true
    );
    consentExists[_code][_version] = Entry(_candidateId, consents[consentCount]._active, true);
    incrementCount();
    emit LogAddedConsent(_candidateId, _code, _detail, _version, _retention, _requesterId, _createTimestamp, _requesterUrl);
  }

  function markAsInactive(string memory _code, uint256 _version, uint256 _updateTimestamp) public onlyOwner {
    require(consentExists[_code][_version]._exists, "Error: Consent does not exist.");
    uint256 _candidateId = consentExists[_code][_version]._idx-1;
    Consent storage consent = consents[_candidateId];
    consent._active = false;
    consent._updateTimestamp = _updateTimestamp;
    consents[_candidateId] = consent;
    consentExists[_code][_version]._active = false;
    emit LogInactivatedConsent(_candidateId, _code, _version, _updateTimestamp);
  }

  function incrementCount() internal {
    consentCount += 1;
  }

  function getConsent(string memory _code, uint256 _version) public override view returns (Consent memory) {
    require(consentExists[_code][_version]._exists, "Error: Consent does not exist.");
    uint256 _candidateId = consentExists[_code][_version]._idx-1;
    Consent storage lConsent = consents[_candidateId];
    return lConsent;
  }

  // return Array of structure
  function getActiveConsents() public view returns (Consent[] memory) {
    Consent[] memory lConsents = new Consent[](consentCount);
    for (uint256 i = 0; i < consentCount; i++) {
      Consent storage lConsent = consents[i];
      if (lConsent._active) {
        lConsents[i] = lConsent;
      }
    }
    return lConsents;
  }
}
