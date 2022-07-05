// SPDX-License-Identifier: MIT
pragma solidity > 0.6.1 < 0.9.0;

import "./libraries/provableAPI.sol";
import "./libraries/stringUtils.sol";
import "./DataSubjectConsentContract.sol";
import "./IDataSubjectConsentContract.sol";
import "./IDataAccessRequestContract.sol";

/// @author Neda Peyrone
/// @dev This solidity is used to manage request participants to access personal data into a blockchain.
contract DataAccessRequestContract is IDataAccessRequestContract, usingProvable {
  mapping(bytes32 => bool) validIds;
  mapping(string => DataAccessRequest) public dataAccessRequests;
  mapping(string => bool) requestExists;

  address owner;
  uint private amount;
  IDataSubjectConsentContract dataSubjectConsentContract;

  event LogSubmittedRequest(string _requestId, string _pseudonym, string _consentCode, uint256 _consentVersion,
    address indexed _responderId, uint256 _createTimestamp, string _dataTransferUrl);
  event LogFiredResponderCallback(string _requestId, string _pseudonym, string _consentCode, uint256 _consentVersion,
    string _responderUrl, bytes32 _queryId, string _message);
  event LogReturnedResponderCallback(bytes32 _queryId, string _result);

  constructor(address _dataSubjectContractAddress) payable {
		OAR = OracleAddrResolverI(0x6f485C8BF6fc43eA212E93BBF8ce046C7f1cb475);
    owner = msg.sender;
    dataSubjectConsentContract = DataSubjectConsentContract(_dataSubjectContractAddress);
  }

  modifier validConsent(
    string memory _pseudonym, 
    string memory _consentCode, 
    uint256 _consentVersion,
    address _responderId
  ) {
    bool expired = dataSubjectConsentContract.isConsentValid(_pseudonym, _consentCode, _consentVersion, _responderId);
    require(!expired, "Error: The data subject's consent has been expired.");
    _;
  }

  function submitRequest(
    string memory _requestId,
    string memory _pseudonym,
    string memory _consentCode,
    uint256 _consentVersion,
    address _responderId,
    uint256 _createTimestamp,
    string memory _dataTransferUrl
  ) public validConsent(_pseudonym, _consentCode, _consentVersion, _responderId) {
    IDataSubjectConsentContract.DataSubjectConsent memory dataSubjectConsent = 
      dataSubjectConsentContract.getDataSubjectConsent(_pseudonym, _consentCode, _consentVersion, _responderId);
    require(!requestExists[_requestId], "Error: Duplicate Request ID.");
    dataAccessRequests[_requestId] = DataAccessRequest(
      _requestId,
      _pseudonym,
      _consentCode,
      _consentVersion,
      _responderId,
      _createTimestamp,
      _dataTransferUrl
    );
    requestExists[_requestId] = true;
    emit LogSubmittedRequest(_requestId, _pseudonym, _consentCode, _consentVersion, _responderId, _createTimestamp, _dataTransferUrl);
    callbackResponder(_requestId, _pseudonym, _consentCode, _consentVersion, dataSubjectConsent._responderUrl);
  }

  // return Single structure
  function getDataAccessRequest(string memory _requestId) public override view returns (DataAccessRequest memory) {
    require(requestExists[_requestId], "Error: Request ID does not exist.");
    DataAccessRequest storage lDataAccessRequest = dataAccessRequests[_requestId];
    bool expired = dataSubjectConsentContract.isConsentValid(
      lDataAccessRequest._pseudonym, 
      lDataAccessRequest._consentCode, 
      lDataAccessRequest._consentVersion,
      lDataAccessRequest._responderId
    );
    require(!expired, "Error: The data subject's consent has been expired.");
    return lDataAccessRequest;
  }

  function callbackResponder(
    string memory requestId,
    string memory pseudonym, 
    string memory consentCode,
    uint256 consentVersion,
    string memory responderUrl
  ) public payable {
    if (provable_getPrice("URL") > address(this).balance) {
      emit LogFiredResponderCallback(requestId, pseudonym, consentCode, consentVersion, responderUrl, 
        "", "Error: Not enough ether in contract, please add more.");
    } else {
      string memory queryUrl = strConcat("json(", responderUrl, ").statusResponse.code");

      string memory param1 = strConcat('{"request_id":"', requestId, '",');
      string memory param2 = strConcat('"pseudonym":"', pseudonym, '",');
      string memory param3 = strConcat('"consent_code":"', consentCode, '",');
      string memory param4 = strConcat('"consent_version":"', StringUtils.uint2str(consentVersion), '"}');
      string memory jsonString = strConcat(param1, param2, param3, param4);

      bytes32 queryId = provable_query("URL", queryUrl, jsonString);
      validIds[queryId] = true;
      emit LogFiredResponderCallback(requestId, pseudonym, consentCode, consentVersion, responderUrl, queryId, 
        "Provable query was sent, standing by for the answer.");
    }
  }

  function __callback(bytes32 myid, string memory result) public override {
    require(validIds[myid], "Error: Provable query IDs do not match, no valid call was made to provable_query().");
    require(msg.sender == provable_cbAddress(), "Error: Calling address does match usingProvable contract address.");
    validIds[myid] = false;
    emit LogReturnedResponderCallback(myid, result);
  }

  function deposit() public payable {
    amount += msg.value;
  }
}