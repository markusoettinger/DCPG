from datetime import datetime
import pandas as pd
from web3 import Web3, HTTPProvider
import logging as log
t = "%d-%m-%Y%H-%M-%S"
log.basicConfig(filename=f'logs/{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.log', level=log.INFO)
log.info(f"{datetime.now().strftime(t)}-------- Simulation started")


class W3Library:
    def __init__(self, should_log=False):
        self.web3 = self.connect()
        self.contract = self.connectContract()
        self.accounts = {}


    def connect(self, rpc_server='HTTP://127.0.0.1:7545'):
        try:
            web3 = Web3(HTTPProvider(rpc_server))
            log.info(f"{datetime.now().strftime(t)}-------- connected to rpc-server: {rpc_server}")
            web3.eth.defaultAccount = web3.eth.accounts[0]
            log.info(f"{datetime.now().strftime(t)}-------- Default account: {web3.eth.accounts[0]}")
            return web3
        except Exception as e:
            print("Error connecting")
            log.info(f"{datetime.now().strftime(t)}-------- Error connecting")
            return False

    def connectContract(self):
        contractaddress = '0x23A03E0B5fE109eFa662C8324AFF749F9BBB24da'
        contractabi = '[    {      "inputs": [        {          "internalType": "string",          "name": "station",          "type": "string"        }      ],      "stateMutability": "nonpayable",      "type": "constructor"    },    {      "inputs": [        {          "internalType": "uint256",          "name": "",          "type": "uint256"        }      ],      "name": "chargingprocesses",      "outputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "address",          "name": "chargee",          "type": "address"        },        {          "internalType": "uint256",          "name": "startTime",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "estimatedDuration",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "availableFlex",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "desiredWh",          "type": "uint256"        }      ],      "stateMutability": "view",      "type": "function",      "constant": true    },    {      "inputs": [],      "name": "godwin",      "outputs": [        {          "internalType": "address",          "name": "",          "type": "address"        }      ],      "stateMutability": "view",      "type": "function",      "constant": true    },    {      "inputs": [],      "name": "getChargingProcessesLength",      "outputs": [        {          "internalType": "uint256",          "name": "",          "type": "uint256"        }      ],      "stateMutability": "nonpayable",      "type": "function"    },    {      "inputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "uint256",          "name": "endTime",          "type": "uint256"        },        {          "internalType": "int256",          "name": "flexFlow",          "type": "int256"        },        {          "internalType": "uint256",          "name": "chargedWh",          "type": "uint256"        }      ],      "name": "stopCharging",      "outputs": [],      "stateMutability": "nonpayable",      "type": "function"    },    {      "inputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "uint256",          "name": "startTime",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "estimatedDuration",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "desiredWh",          "type": "uint256"        }      ],      "name": "startCharging",      "outputs": [],      "stateMutability": "payable",      "type": "function",      "payable": true    }  ]'
        log.info(f"{datetime.now().strftime(t)}-------- Connected to SmartContract with address: {contractaddress}")
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
        log.info(f"{datetime.now().strftime(t)}-------- Transaction of {value*1e-18} ether from {fromAddress} to {toAddress}")
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
            log.info(f"{datetime.now().strftime(t)}-------- New account {newAddress} created for user {userId}")
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
        log.info(f"{datetime.now().strftime(t)}-------- User {userId} started charging at {chargerId} and payed {flex} to the contract. Simulation Time: {str(startTime)}")
        return flex, transactionHash

    def stopCharging(self, userId, endTime, flexFlow, chargedkWh):
        chargedWh = int(chargedkWh * 1000)
        flexFlow = int(flexFlow * 1e18)
        transactionHash = self.contract.functions.stopCharging(userId, self.accounts[userId]["chargerId"], int(endTime.timestamp()), flexFlow, chargedWh).transact()
        self.web3.eth.waitForTransactionReceipt(transactionHash)
        self.accounts[userId]["chargerId"] = None
        log.info(f"{datetime.now().strftime(t)}-------- User {userId} stopped charging at {chargerId}. Simulation Time: {str(startTime)}")
        return transactionHash

    def inCharging(self):
        numberCharging = self.contract.functions.getChargingProcessesLength().call()
        processes = []
        varNames = ["userID", "chargerID", "chargee", "startTime", "estimatedDuration", "availableFlex", "desiredWh"]
        for i in range(numberCharging):
            process = self.contract.functions.chargingprocesses(i).call()
            processes.append(dict(zip(varNames, process)))
        log.info(f"{datetime.now().strftime(t)}-------- ")
        return processes
