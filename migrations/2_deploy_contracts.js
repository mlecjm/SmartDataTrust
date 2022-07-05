const ConsentContract = artifacts.require("ConsentContract");
const DataFieldContract = artifacts.require("DataFieldContract");
const DataSubjectConsentContract = artifacts.require("DataSubjectConsentContract");
const DataAccessRequestContract = artifacts.require("DataAccessRequestContract");
const DataAccessResponseContract = artifacts.require("DataAccessResponseContract");

const Migrations = artifacts.require("Migrations");
const StringUtils = artifacts.require("libraries/stringUtils");

var adapter = Migrations.interfaceAdapter;
const web3 = adapter.web3;

module.exports = async function(deployer, network, accounts) {
	deployer.deploy(StringUtils, {from: accounts[1]})
	deployer.link(StringUtils, DataSubjectConsentContract);

  // deploy ConsentContract first
  deployer.deploy(ConsentContract, {from: accounts[2]}).then(async () => {
    // get JS instance of deployed contract
    const consentInst = await ConsentContract.deployed(); 
    // pass its address as argument for DataSubjectConsentContract's constructor
    await deployer.deploy(DataSubjectConsentContract, consentInst.address, {from: accounts[3]}); 

    // pass its address as argument for DataFieldContract's constructor
    await deployer.deploy(DataFieldContract, consentInst.address, {from: accounts[4]}); 

    const dataSubjectConsentInst = await DataSubjectConsentContract.deployed(); 
    // pass its address as argument for DataAccessRequestContract's constructor
    await deployer.deploy(DataAccessRequestContract, dataSubjectConsentInst.address, {from: accounts[5]}); 

    const dataAccessRequestInst = await DataAccessRequestContract.deployed(); 
    // pass its address as argument for DataAccessResponseContract's constructor
    await deployer.deploy(DataAccessResponseContract, dataSubjectConsentInst.address, dataAccessRequestInst.address, {from: accounts[6]});

    const dataAccessResponseInst = await DataAccessResponseContract.deployed();

    var s = 10;
    await dataSubjectConsentInst.deposit({
      from: accounts[9],
      value: web3.utils.toWei(s.toString(), "ether"),
      gas: "4712388"
    });

    await dataAccessRequestInst.deposit({
      from: accounts[9],
      value: web3.utils.toWei(s.toString(), "ether"),
      gas: "4712388"
    });

    await dataAccessResponseInst.deposit({
      from: accounts[9],
      value: web3.utils.toWei(s.toString(), "ether"),
      gas: "4712388"
    });

    let oraclizeAddressBalance = await web3.eth.getBalance('0x6f485C8BF6fc43eA212E93BBF8ce046C7f1cb475');
    console.log(`O:--Get OraclizeAddress's Balance--:address/0x6f485C8BF6fc43eA212E93BBF8ce046C7f1cb475:balance/${oraclizeAddressBalance}`);

    let dataSubjectConsentBalance = await web3.eth.getBalance(dataSubjectConsentInst.address);
    console.log(`O:--Get DataSubjectConsentContract's Balance--:address/${dataSubjectConsentInst.address}:balance/${dataSubjectConsentBalance}`);

    let dataAccessRequestBalance = await web3.eth.getBalance(dataAccessRequestInst.address);
    console.log(`O:--Get DataAccessRequestContract's Balance--:address/${dataAccessRequestInst.address}:balance/${dataAccessRequestBalance}`);

    let dataAccessResponseBalance = await web3.eth.getBalance(dataAccessResponseInst.address);
    console.log(`O:--Get DataAccessResponseContract's Balance--:address/${dataAccessResponseInst.address}:balance/${dataAccessResponseBalance}`);
	}
)};