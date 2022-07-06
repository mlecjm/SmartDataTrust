# SmartDataTrust

The SmartDataTrust is a platform that implemented a Python REST API with Smart Contracts written in Solidity to enable consent management in data sharing. The platform has completed development and integration tests performed on a local blockchain with Ganache. It provides essential technical insights into implementing consent management functionality among distributed services.

## Pre-requisites
The platform consists of Smart Contracts and the Python code that implements methods followed by our proposed model, [Data Sharing State Machine (DSSM)](https://github.com/cucpbioinfo/BlockchainBasedDataSharing), incorporating Privacy by Design (PbD) to ensure compliance with the General Data Protection Regulation (GDPR) requirements.

To deploy and test these Smart Contracts, we use Truffle and Ganache.

* [Truffle](https://www.trufflesuite.com/truffle) is a development environment and testing framework for Smart Contracts for blockchains using the Ethereum Virtual Machine (EVM).
* [Ganache](https://www.trufflesuite.com/ganache) is an Ethereum-like network emulator that enables a personal Ethereum blockchain on the local network to run execute commands and inspect the state of the blockchain.

### Requirements
------------
To install Truffle and Ganache, you can install them through npm, but you first need to install [Node](https://nodejs.org/en/) on your local machine.

```bash
sudo npm install -g truffle ganache-cli
```

### Installation
------------
* Clone this repository to create a local copy on your computer.
* Open a terminal and `cd` to SmartDataTrust folder in which `package.json` is saved and run:

```bash
npm install
```

The above command is used to install the dependencies in the local node_modules folder in your project. Then, you can start using [ethereum-bridge](https://github.com/provable-things/ethereum-bridge).

The following command is used to start a local blockchain.
```bash
npm run chain
```

The following command is used to enable an oraclize service, which handles API calls outside the blockchain.
```bash
npm run bridge
```

The following command is used to deploy Smart Contracts on the blockchain using Truffle.
```bash
truffle migrate
```

The following command is used to install Python dependencies.
```bash
pip install -r requirements.txt
```

After successfully deploying Smart Contracts on the blockchain, you need to update Smart Contracts' address into `config.yml` within `resources` folder. Then, you can start a Python REST API using the following command.
```bash
python main.py
```

To run unit tests, you can find them inside the `tests` folder. Moreover, for testing the callback URL through ethereum-bridge, you first need to enable SSL for localhost accessible to the outside. We recommended [ngrok](https://ngrok.com), which is free and easy to use.

In addition, you need to run unit tests in a specific order. An example of executing a unit test is as follows:
```bash
python -m unittest tests/test_01_requester_add_consent.py
```

------------

## Project Structure
```
/
├─api/       			                  Contains all Python code
│  ├─business_logic
│  │    ├─consent_service.py
│  │    ├─data_access_request_service.py
│  │    ├─data_access_response_service.py
│  │    ├─data_field_service.py
│  │    ├─data_subject_service.py
│  ├─configuration/
│  │    ├─app_config.py
│  │    ├─blockchain_config.py
│  ├─connector/
│  │    ├─blockchain_connector.py
│  │    ├─rest_client.py
│  ├─constant/
│  │    ├─message_code.py
│  ├─controller/
│  │    ├─consent_controller.py
│  │    ├─data_access_request_controller.py
│  │    ├─data_access_response_controller.py
│  │    ├─data_subject_controller.py
│  ├─domain/
│  │    ├─consent.py
│  │    ├─data_access_request.py
│  │    ├─data_access_response.py
│  │    ├─data_field.py
│  │    ├─data_subject_consent.py
│  │    ├─header.py
│  │    ├─server_reponse.py
│  │    ├─status_response.py
│  ├─exception/
│  │    ├─service_exception.py
│  │    ├─validation_exception.py
│  ├─schema/
│  ├─util/
├─bootstrap.py 	
├─contracts/ 			                 Directory for Solidity contracts
│  ├─libraries/
│  │    ├─provableAPI.py
│  │    ├─stringUtils.py       
│  ├─ConsentContract.sol 		            
│  ├─DataAccessRequestContract.sol 		  
│  ├─DataAccessResponseContract.sol 		  
│  ├─DataFieldContract.sol 		  
│  ├─DataSubjectConsentContract.sol 		  
│  ├─IConsentContract.sol
│  ├─IDataAccessRequestContract.sol 
│  ├─IDataFieldContract.sol 
│  ├─IDataSubjectConsentContract.sol 
│  ├─Migrations.sol 
├─migrations/ 			                 Directory for scriptable deployment files
│  ├─1_initial_migrations.js 	
│  ├─2_deploy_contracts.js 		         Deploys Smart Contracts
├─resources/
│  ├─config.yaml 	                     Contains Smart Contracts' address 
├─tests/ 				                 Directory for test files for testing your application and contracts
├─main.py 				                 A Python srcipt to start a Python REST API
├─package.json				             Contains NPM dependencies
├─requirements.txt 				         Contains Python dependencies
├─truffle-config.js 	                 Truffle configuration file
```

------------

## Author

* **Neda Peyrone** - [peyrone](https://github.com/peyrone)