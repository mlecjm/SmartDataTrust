// SPDX-License-Identifier: MIT
pragma solidity > 0.6.1 < 0.9.0;

import "./libraries/provableAPI.sol";
import "./DataSubjectConsentContract.sol";
import "./DataAccessRequestContract.sol";

/// @author Neda Peyrone
/// @dev This solidity is used to manage providers response to participants' data into a blockchain.
contract DataAccessResponseContract is usingProvable {
  mapping(bytes32 => bool) validIds;
  mapping(string => DataAccessResponse) public dataAccessResponses;
  mapping(string => bool) responseExists;

  address owner;
  uint private amount;

  event LogSubmittedResponse(string _responseId, string _requestId, string _acceptedFlag, string _acceptedMessage,
    uint256 _createTimestamp, string _responderUrl);
  event LogFiredDataTranferCallback(string _responseId, string _responderUrl, string _transferUrl,
    bytes32 _queryId, string _message);
  event LogReturnedDataTransferCallback(bytes32 _queryId, string _result);

  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }

  IDataSubjectConsentContract dataSubjectConsentContract;
  IDataAccessRequestContract dataAccessRequestContract;

  struct DataAccessResponse {
    string _responseId;
    string _requestId;
    string _acceptedFlag;
    string _acceptedMessage;
    uint256 _createTimestamp;
    string _callbackUrl;
  }

  constructor(address _dataSubjectConsentContractAddress, address _dataAccessRequestContractAddress) payable {
		OAR = OracleAddrResolverI(0x6f485C8BF6fc43eA212E93BBF8ce046C7f1cb475);
    owner = msg.sender;
    dataSubjectConsentContract = DataSubjectConsentContract(_dataSubjectConsentContractAddress);
    dataAccessRequestContract = DataAccessRequestContract(_dataAccessRequestContractAddress);
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

  function submitResponse(
    string memory _responseId,
    string memory _requestId,
    string memory _acceptedFlag,
    string memory _acceptedMessage,
    uint256 _createTimestamp,
    string memory _responderUrl
  ) public {
    require(!responseExists[_responseId], "Error: Duplicate Response ID.");
    IDataAccessRequestContract.DataAccessRequest memory lDataAccessRequest = dataAccessRequestContract.getDataAccessRequest(_requestId);
    bool expired = dataSubjectConsentContract.isConsentValid(
      lDataAccessRequest._pseudonym, 
      lDataAccessRequest._consentCode, 
      lDataAccessRequest._consentVersion,
      lDataAccessRequest._responderId
    );
    require(!expired, "Error: The data subject's consent has been expired.");
    dataAccessResponses[_responseId] = DataAccessResponse(
      _responseId,
      _requestId,
      _acceptedFlag,
      _acceptedMessage,
      _createTimestamp,
      _responderUrl
    );
    responseExists[_responseId] = true;
    emit LogSubmittedResponse(_responseId, _requestId, _acceptedFlag, _acceptedMessage, _createTimestamp, _responderUrl);
    callbackDataTransfer(_responseId, _responderUrl, lDataAccessRequest._dataTransferUrl);
  }

  function callbackDataTransfer(
    string memory responseId,
    string memory responderUrl,
    string memory transferUrl
  ) public payable {
    if (provable_getPrice("URL") > address(this).balance) {
      emit LogFiredDataTranferCallback(responseId, responderUrl, transferUrl, "", "Error: Not enough ether in contract, please add more.");
    } else {
      string memory queryUrl = strConcat("json(", responderUrl, ").statusResponse.code");

      string memory param1 = strConcat('{"response_id":"', responseId, '",');
      string memory param2 = strConcat('"transfer_url":"', transferUrl, '"}');
      string memory jsonString = strConcat(param1, param2);

      bytes32 queryId = provable_query("URL", queryUrl, jsonString);
      validIds[queryId] = true;
      emit LogFiredDataTranferCallback(responseId, responderUrl, transferUrl, queryId, "Provable query was sent, standing by for the answer.");
    }
  }

  function __callback(bytes32 myid, string memory result) public override {
    require(validIds[myid], "Error: Provable query IDs do not match, no valid call was made to provable_query().");
    require(msg.sender == provable_cbAddress(), "Error: Calling address does match usingProvable contract address.");
    validIds[myid] = false;
    // if (msg.sender != provable_cbAddress()) revert();
    emit LogReturnedDataTransferCallback(myid, result);
  }

  function deposit() public payable {
    amount += msg.value;
  }
}