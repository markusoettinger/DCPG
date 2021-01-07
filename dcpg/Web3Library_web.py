import pandas as pd
from web3 import Web3, HTTPProvider


class W3Library:
    def __init__(self, should_log=False):
        self.log = []
        self.should_log = should_log
        self.web3 = self.connect()
        self.contract = self.connectContract()
        self.accounts = {}


    def connect(self, rpc_server='HTTP://127.0.0.1:7545'):
        try:
            print("trying to connect")
            print(rpc_server)
            web3 = Web3(HTTPProvider(rpc_server))
            print("did connect")
            print(web3.eth.accounts)
            web3.eth.defaultAccount = web3.eth.accounts[0]
            print("set account")
            if self.should_log:
                self.log.append(f'Connection to {rpc_server} was successful')
            print("did logging")
            return web3
        except Exception as e:
            print("Error connecting")

            self.log.append(f'Connection to {rpc_server} failed with Error: {e}')
            return False

    def connectContract(self):
        contractaddress = '0x23A03E0B5fE109eFa662C8324AFF749F9BBB24da'
        contractabi = '[    {      "inputs": [        {          "internalType": "string",          "name": "station",          "type": "string"        }      ],      "stateMutability": "nonpayable",      "type": "constructor"    },    {      "inputs": [        {          "internalType": "uint256",          "name": "",          "type": "uint256"        }      ],      "name": "chargingprocesses",      "outputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "address",          "name": "chargee",          "type": "address"        },        {          "internalType": "uint256",          "name": "startTime",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "estimatedDuration",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "availableFlex",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "desiredWh",          "type": "uint256"        }      ],      "stateMutability": "view",      "type": "function",      "constant": true    },    {      "inputs": [],      "name": "godwin",      "outputs": [        {          "internalType": "address",          "name": "",          "type": "address"        }      ],      "stateMutability": "view",      "type": "function",      "constant": true    },    {      "inputs": [],      "name": "getChargingProcessesLength",      "outputs": [        {          "internalType": "uint256",          "name": "",          "type": "uint256"        }      ],      "stateMutability": "nonpayable",      "type": "function"    },    {      "inputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "uint256",          "name": "endTime",          "type": "uint256"        },        {          "internalType": "int256",          "name": "flexFlow",          "type": "int256"        },        {          "internalType": "uint256",          "name": "chargedWh",          "type": "uint256"        }      ],      "name": "stopCharging",      "outputs": [],      "stateMutability": "nonpayable",      "type": "function"    },    {      "inputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "uint256",          "name": "startTime",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "estimatedDuration",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "desiredWh",          "type": "uint256"        }      ],      "name": "startCharging",      "outputs": [],      "stateMutability": "payable",      "type": "function",      "payable": true    }  ]'
        if self.should_log:
            self.log.append(f'Contract connection to {contractaddress} was successful')
        return self.web3.eth.contract(address=self.web3.toChecksumAddress(contractaddress), abi=contractabi)

    def getBalance(self, address):
        return self.web3.eth.getBalance(address)

    def getBalanceForUser(self, userId):
        if userId in self.accounts:
            return self.web3.eth.getBalance(self.accounts[userId]["address"])
        raise IndexError("UserId not known in Accounts")

    def transact(self, toAddress, fromAddress, value):
        value = int(value)
        if fromAddress == 'Faucet':
            ret = self.web3.eth.sendTransaction({'to': toAddress, 'value': value})
        else:
            ret = self.web3.eth.sendTransaction({'to': toAddress, 'from': fromAddress, 'value': value})
        if self.should_log:
            self.log.append(f'Transacted {value} from {fromAddress} to {toAddress}')
        return Web3.toHex(ret)

    def newAccount(self, userId):
        # df_accounts = pd.readcsv('accountList.csv')
        if userId not in self.accounts:
            newAddress = self.web3.geth.personal.new_account(str(userId))
            self.web3.geth.personal.unlockAccount(newAddress, str(userId), 0)
            self.accounts[userId] = {'userID': userId, 'address': newAddress, "chargerId": None}
            # df_accounts.to_csv('accountList.csv')
            # FaucetTransaction
            self.transact(newAddress, 'Faucet', 3e20)  # need to be changed to highest Flexpayer amount
            if self.should_log:
                self.log.append(f'Account of {userId} at Address {newAddress} created')
        return newAddress

    def startCharging(self, userId, chargerId, startTime, estimateDuration, desiredkWh, flex=None):
        P_charger = 3.5  # kW --> example for calculating max Flex to pay
        # estimateDuration evtl. umwandeln
        fromAddress = self.accounts[userId]["address"]
        self.accounts[userId]["chargerId"] = chargerId
        av_balance = self.getBalance(fromAddress)
        # Check balance for amount available
        if flex is None:
            flexWh = desiredkWh - (P_charger * (estimateDuration.total_seconds() / 3600)) + 10
            flex = int(flexWh * 1e18)
        if flex > av_balance:
            flex = av_balance
        if flex < 0:
            flex = 0

        desiredWh = int(desiredkWh * 1000)
        transactionHash = self.contract.functions.startCharging(userId, chargerId, int(startTime.timestamp()),
                                                           int(round(estimateDuration.total_seconds(), 0)),
                                                           desiredWh).transact({'from': fromAddress, 'value': flex})
        self.web3.eth.waitForTransactionReceipt(transactionHash)
        if self.should_log:
            self.log.append(f'{userId} started charging {fromAddress} to {toAddress}')
        return flex, transactionHash

    def stopCharging(self, userId, endTime, flexFlow, chargedkWh):
        chargedWh = int(chargedkWh * 1000)
        flexFlow = int(flexFlow * 1e18)
        transactionHash = self.contract.functions.stopCharging(userId, self.accounts[userId]["chargerId"], int(endTime.timestamp()), flexFlow, chargedWh).transact()
        self.web3.eth.waitForTransactionReceipt(transactionHash)
        self.accounts[userId]["chargerId"] = None

        return transactionHash

    def inCharging(self):
        numberCharging = self.contract.functions.getChargingProcessesLength().call()
        processes = []
        varNames = ["userID", "chargerID", "chargee", "startTime", "estimatedDuration", "availableFlex", "desiredWh"]
        for i in range(numberCharging):
            process = self.contract.functions.chargingprocesses(i).call()
            processes.append(dict(zip(varNames, process)))
        return processes
