from web3 import Web3, HTTPProvider
import pandas as pd
import numpy as np



class w3Library:
    def __init__(self, url=None):
        self.web3 = self.connect(url)
        self.contract = self.connectContract()
        self.accounts = {}

    def connect(rpc_server='HTTP://127.0.0.1:7545'):
        web3 = Web3(HTTPProvider(rpc_server))
        web3.eth.defaultAccount = web3.eth.accounts[0]
        return web3

    def connectContract(self):
        contractaddress = '0x23A03E0B5fE109eFa662C8324AFF749F9BBB24da'
        contractabi = '[    {      "inputs": [        {          "internalType": "string",          "name": "station",          "type": "string"        }      ],      "stateMutability": "nonpayable",      "type": "constructor"    },    {      "inputs": [        {          "internalType": "uint256",          "name": "",          "type": "uint256"        }      ],      "name": "chargingprocesses",      "outputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "address",          "name": "chargee",          "type": "address"        },        {          "internalType": "uint256",          "name": "startTime",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "estimatedDuration",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "availableFlex",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "desiredWh",          "type": "uint256"        }      ],      "stateMutability": "view",      "type": "function",      "constant": true    },    {      "inputs": [],      "name": "godwin",      "outputs": [        {          "internalType": "address",          "name": "",          "type": "address"        }      ],      "stateMutability": "view",      "type": "function",      "constant": true    },    {      "inputs": [],      "name": "getChargingProcessesLength",      "outputs": [        {          "internalType": "uint256",          "name": "",          "type": "uint256"        }      ],      "stateMutability": "nonpayable",      "type": "function"    },    {      "inputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "uint256",          "name": "endTime",          "type": "uint256"        },        {          "internalType": "int256",          "name": "flexFlow",          "type": "int256"        },        {          "internalType": "uint256",          "name": "chargedWh",          "type": "uint256"        }      ],      "name": "stopCharging",      "outputs": [],      "stateMutability": "nonpayable",      "type": "function"    },    {      "inputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "uint256",          "name": "startTime",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "estimatedDuration",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "desiredWh",          "type": "uint256"        }      ],      "name": "startCharging",      "outputs": [],      "stateMutability": "payable",      "type": "function",      "payable": true    }  ]'
        return self.web3.eth.contract(address=self.web3.toChecksumAddress(contractaddress), abi=contractabi)

    def getBalance(self, address):
        return self.web3.eth.getBalance(address)

    def transact(self, toAddress, fromAddress, value):
        value = int(value)
        if fromAddress == 'Faucet':
            ret = self.web3.eth.sendTransaction({'to': toAddress, 'value': value})
        else:
            ret = self.web3.eth.sendTransaction({'to': toAddress, 'from': fromAddress, 'value': value})
        return Web3.toHex(ret)

    def newAccount(self, userId):
        # df_accounts = pd.readcsv('accountList.csv')
        if userId not in self.accounts:
            newAddress = self.web3.geth.personal.new_account(str(userId))
            self.web3.geth.personal.unlockAccount(newAddress, str(userId), 0)
            df_accounts = df_accounts.append({'userID': userId, 'Address': newAddress}, ignore_index=True)
            df_accounts.to_csv('accountList.csv')
            # FaucetTransaction
            self.transact(newAddress, 'Faucet', 3e20)  # need to be changed to highest Flexpayer amount
        return newAddress, df_accounts

    def startCharging(self, contract, df_accounts, userId, chargerId, startTime, estimateDuration, desiredkWh):
        P_charger = 3.5  # kW --> example for calculating max Flex to pay
        # estimateDuration evtl. umwandeln
        flexWh = desiredkWh - (P_charger * (estimateDuration.total_seconds() / 3600)) + 10
        value = int(flexWh * 1e18)
        if value < 0:
            value = 0
        fromAddress = df_accounts[df_accounts.userID == userId].iat[0,1]
        startTime = (startTime - pd.Timestamp("1970-01-01", tz='UTC')) // pd.Timedelta('1s')  # to unix timestamp
        desiredWh = int(desiredkWh * 1000)
        transactionHash = contract.functions.startCharging(userId, chargerId, startTime, int(round(estimateDuration.total_seconds(), 0)),
                                                           desiredWh).transact({'from': fromAddress, 'value': value})
        self.web3.eth.waitForTransactionReceipt(transactionHash)
        return value, transactionHash






def stopCharging(web3, contract, df_accounts, userId, chargerId, endTime, flexFlow, chargedkWh):
    fromAddress = df_accounts[df_accounts.userID == userId].iat[0,1]
    endTime = (endTime - pd.Timestamp("1970-01-01", tz='UTC')) // pd.Timedelta('1s')  # to unix timestamp
    chargedWh = int(chargedkWh * 1000)
    flexFlow = int(flexFlow * 1e18)
    transactionHash = contract.functions.stopCharging(userId, chargerId, endTime, flexFlow, chargedWh).transact()
    web3.eth.waitForTransactionReceipt(transactionHash)
    return transactionHash

def inCharging(contract):
    numberCharging = contract.functions.getChargingProcessesLength().call()
    processes = []
    varNames = ["userID", "chargerID", "chargee", "startTime", "estimatedDuration", "availableFlex", "desiredWh"]
    for i in range(numberCharging):
        process = contract.functions.chargingprocesses(i).call()
        processes.append(dict(zip(varNames, process)))
    return processes