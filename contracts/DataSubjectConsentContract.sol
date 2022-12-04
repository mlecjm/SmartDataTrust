// SPDX-License-Identifier: MIT
pragma solidity >0.6.1 <0.9.0;

import "./ConsentContract.sol";
import "./libraries/provableAPI.sol";
import "./libraries/stringUtils.sol";
import "./IDataSubjectConsentContract.sol";

/// @author Neda Peyrone
/// @dev This solidity is used to manage data subject's consent into a blockchain.
contract DataSubjectConsentContract is IDataSubjectConsentContract, usingProvable {
    mapping(bytes32 => bool) validIds;
    uint256 public dataSubjectConsentCount = 0;
    mapping(uint256 => DataSubjectConsent) public dataSubjectConsents;
    mapping(string => mapping(string => mapping(uint256 => mapping(address => Entry)))) public dataSubjectConsentedActive;

    address owner;
    uint private amount;

    event LogAddedDataSubjectConsent(string _pseudonym, string _consentCode, uint256 _consentVersion, 
      address indexed _responderId, string _acceptedFlag, uint256 _createTimestamp, string _responderUrl);
    event LogFiredRequesterCallback(string _pseudonym, string _consentCode, uint256 _consentVersion, 
      address indexed _responderId, string _requesterUrl, bytes32 _queryId, string _message);
    event LogReturnedRequesterCallback(bytes32 _queryId, string _result);
    event LogRevokedConsent(string _pseudonym, string _consentCode, uint256 _consentVersion, address indexed _responderId,
      uint256 _withdrawnTimestamp);
    event LogRenewedConsent(string _pseudonym, string _consentCode, uint256 _consentVersion, address indexed _responderId,
      uint256 _createTimestamp);

    IConsentContract consentContract;

    struct Entry {
      uint256 _idx;
      bool _exists;
    }

    constructor(address _consentContractAddress) payable {
      // provable_setCustomGasPrice(1000000000);
			OAR = OracleAddrResolverI(0x6f485C8BF6fc43eA212E93BBF8ce046C7f1cb475);
      owner = msg.sender;
      consentContract = ConsentContract(_consentContractAddress);
    }

    function isConsentValid(
      string memory _pseudonym, 
      string memory _consentCode, 
      uint256 _consentVersion,
      address _responderId
    ) public override view returns(bool) {
      DataSubjectConsent memory dataSubjectConsent = getDataSubjectConsent(_pseudonym, _consentCode, _consentVersion, _responderId);
      IConsentContract.Consent memory consent = consentContract.getConsent(_consentCode, _consentVersion);
      uint256 expiryTimestamp = dataSubjectConsent._createTimestamp + (consent._dataRetention * 1 days);
      return block.timestamp > expiryTimestamp;
    }

    function addDataSubjectConsent(
      string memory _pseudonym,
      string memory _consentCode,
      uint256 _consentVersion,
      address _responderId,
      string memory _acceptedFlag,
      uint256 _createTimestamp,
      string memory _withdrawnFlag,
      uint256 _withdrawnTimestamp,
      string memory _responderUrl
    ) public {
      require(!dataSubjectConsentedActive[_pseudonym][_consentCode][_consentVersion][_responderId]._exists, 
        "Error: The data subject's consent has been given.");
      IConsentContract.Consent memory consent = consentContract.getConsent(_consentCode, _consentVersion);
      uint256 _candidateId = dataSubjectConsentCount+1;
      dataSubjectConsents[dataSubjectConsentCount] = DataSubjectConsent(
        _candidateId,
        _pseudonym,
        consent._consentCode,
        consent._consentVersion,
        _responderId,
        _acceptedFlag,
        _createTimestamp,
        _withdrawnFlag,
        _withdrawnTimestamp,
        _responderUrl
      );
      dataSubjectConsentedActive[_pseudonym][_consentCode][_consentVersion][_responderId] = Entry(dataSubjectConsents[dataSubjectConsentCount]._id, true);
      incrementCount();
      emit LogAddedDataSubjectConsent(_pseudonym, _consentCode, _consentVersion, _responderId, _acceptedFlag, _createTimestamp, _responderUrl);
      callbackRequester(_pseudonym, consent._consentCode, consent._consentVersion, _responderId, consent._requesterUrl);
    }

    function incrementCount() internal {
      dataSubjectConsentCount += 1;
    }

    function getDataSubjectConsent(
      string memory _pseudonym, 
      string memory _consentCode, 
      uint256 _consentVersion,
      address _responderId
    ) public override view returns (DataSubjectConsent memory) {
      Entry memory consentedActive = dataSubjectConsentedActive[_pseudonym][_consentCode][_consentVersion][_responderId];
      require(consentedActive._exists, "Error: The data subject's consent does not exist.");
      DataSubjectConsent storage lDataSubjectConsent = dataSubjectConsents[consentedActive._idx-1];
      return lDataSubjectConsent;
    }

    // return Array of structure
    function getDataSubjectConsents() public view returns (DataSubjectConsent[] memory) {
      DataSubjectConsent[] memory lDataSubjectConsents = new DataSubjectConsent[](dataSubjectConsentCount);
      for (uint256 i = 0; i < dataSubjectConsentCount; i++) {
        DataSubjectConsent storage lDataSubjectConsent = dataSubjectConsents[i];
        lDataSubjectConsents[i] = lDataSubjectConsent;
      }
      return lDataSubjectConsents;
    }

		function revokeConsent(
			string memory _pseudonym, 
      string memory _consentCode, 
      uint256 _consentVersion,
      address _responderId,
      uint256 _withdrawnTimestamp
		) public {
			Entry memory consentedActive = dataSubjectConsentedActive[_pseudonym][_consentCode][_consentVersion][_responderId];
      require(consentedActive._exists, "Error: The data subject's consent does not exist.");
      DataSubjectConsent memory dataSubjectConsent = dataSubjectConsents[consentedActive._idx-1];
      dataSubjectConsent._withdrawnFlag = "Y";
      dataSubjectConsent._withdrawnTimestamp = _withdrawnTimestamp;
      dataSubjectConsents[consentedActive._idx-1] = dataSubjectConsent;
			consentedActive._exists = false;
      dataSubjectConsentedActive[_pseudonym][_consentCode][_consentVersion][_responderId] = consentedActive;
      emit LogRevokedConsent(_pseudonym, _consentCode, _consentVersion, _responderId, _withdrawnTimestamp);
		}

		function renewConsent(
			string memory _pseudonym, 
      string memory _consentCode, 
      uint256 _consentVersion,
      address _responderId,
			uint256 _createTimestamp
		) public {
			DataSubjectConsent memory dataSubjectConsent = getDataSubjectConsent(_pseudonym, _consentCode, _consentVersion, _responderId);
			dataSubjectConsent._createTimestamp = _createTimestamp;
			Entry memory consentedActive = dataSubjectConsentedActive[_pseudonym][_consentCode][_consentVersion][_responderId];
			dataSubjectConsents[consentedActive._idx-1] = dataSubjectConsent;
      emit LogRenewedConsent(_pseudonym, _consentCode, _consentVersion, _responderId, _createTimestamp);
		}

    function callbackRequester(
      string memory pseudonym, 
      string memory consentCode,
      uint256 consentVersion,
      address responderId,
      string memory requesterUrl
    ) public payable {
      if (provable_getPrice("URL") > address(this).balance) {
        emit LogFiredRequesterCallback(pseudonym, consentCode, consentVersion, responderId, requesterUrl, 
          "", "Error: Not enough ether in contract, please add more.");
				require(false, "Error: Not enough ether in contract, please add more.");
      } else {
        string memory queryUrl = strConcat("json(", requesterUrl, ").statusResponse.code");

        string memory param1 = strConcat('{"pseudonym":"', pseudonym, '",');
        string memory param2 = strConcat('"consent_code":"', consentCode, '",');
        string memory param3 = strConcat('"responder_id":"', StringUtils.toString(responderId), '",');
        string memory param4 = strConcat('"consent_version":"', StringUtils.uint2str(consentVersion), '"}');
        string memory jsonString = strConcat(param1, param2, param3, param4);

        bytes32 queryId = provable_query("URL", queryUrl, jsonString);
        validIds[queryId] = true;
        emit LogFiredRequesterCallback(pseudonym, consentCode, consentVersion, responderId, requesterUrl, queryId, 
          "Provable query was sent, standing by for the answer.");
      }
    }

    function __callback(bytes32 myid, string memory result) public override {
      require(validIds[myid], "Error: Provable query IDs do not match, no valid call was made to provable_query().");
      require(msg.sender == provable_cbAddress(), "Error: Calling address does match usingProvable contract address.");
      validIds[myid] = false;
      // if (msg.sender != provable_cbAddress()) revert();
      emit LogReturnedRequesterCallback(myid, result);
    }

    function deposit() public payable {
      amount += msg.value;
    }
}
