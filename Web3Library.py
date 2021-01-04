# Library with functions of the Web3 Library to connect and interact with the blockchain and smart contract on the BC

from web3 import Web3, HTTPProvider
import pandas as pd
import numpy as np


def connect(ganache):
    if ganache:
        rpc_server = 'HTTP://127.0.0.1:7545'
    else:
        rpc_server = ganache
    web3 = Web3(HTTPProvider(rpc_server))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    return web3


def getBalance(web3, address):
    return web3.eth.getBalance(address)


def transact(web3, toAddress, fromAddress, value):
    value = int(value)
    if fromAddress == 'Faucet':
        ret = web3.eth.sendTransaction({'to': toAddress, 'value': value})
    else:
        ret = web3.eth.sendTransaction({'to': toAddress, 'from': fromAddress, 'value': value})
    return Web3.toHex(ret)


def newAccount(web3, userId, df_accounts):
    # df_accounts = pd.readcsv('accountList.csv')
    if userId not in df_accounts["userID"]:
        newAddress = web3.geth.personal.new_account(str(userId))
        web3.geth.personal.unlockAccount(newAddress, str(userId), 0)
        df_accounts = df_accounts.append({'userID': userId, 'Address': newAddress}, ignore_index=True)
        df_accounts.to_csv('accountList.csv')
        # FaucetTransaction
        transact(web3, newAddress, 'Faucet', 3e20)  # need to be changed to highest Flexpayer amount
    return web3, newAddress, df_accounts


def connectContract(web3):
    contractaddress = '0x2bD7D2F34990E15816388ECd5b25eed8707623C9'
    contractabi = '[    {      "inputs": [        {          "internalType": "string",          "name": "station",          "type": "string"        }      ],      "stateMutability": "nonpayable",      "type": "constructor"    },    {      "inputs": [        {          "internalType": "uint256",          "name": "",          "type": "uint256"        }      ],      "name": "chargingprocesses",      "outputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "address",          "name": "chargee",          "type": "address"        },        {          "internalType": "uint256",          "name": "startTime",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "estimatedDuration",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "availableFlex",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "desiredWh",          "type": "uint256"        }      ],      "stateMutability": "view",      "type": "function",      "constant": true    },    {      "inputs": [],      "name": "godwin",      "outputs": [        {          "internalType": "address",          "name": "",          "type": "address"        }      ],      "stateMutability": "view",      "type": "function",      "constant": true    },    {      "inputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "uint256",          "name": "endTime",          "type": "uint256"        },        {          "internalType": "int256",          "name": "flexFlow",          "type": "int256"        },        {          "internalType": "uint256",          "name": "chargedWh",          "type": "uint256"        }      ],      "name": "stopCharging",      "outputs": [],      "stateMutability": "nonpayable",      "type": "function"    },    {      "inputs": [        {          "internalType": "string",          "name": "userID",          "type": "string"        },        {          "internalType": "string",          "name": "chargerID",          "type": "string"        },        {          "internalType": "uint256",          "name": "startTime",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "estimatedDuration",          "type": "uint256"        },        {          "internalType": "uint256",          "name": "desiredWh",          "type": "uint256"        }      ],      "name": "startCharging",      "outputs": [],      "stateMutability": "payable",      "type": "function",      "payable": true    }  ]'
    return web3.eth.contract(address=web3.toChecksumAddress(contractaddress), abi=contractabi)


def startCharging(web3, contract, df_accounts, userId, chargerId, startTime, estimateDuration, desiredkWh):
    P_charger = 3.5  # kW --> example for calculating max Flex to pay
    # estimateDuration evtl. umwandeln
    flexWh = desiredkWh - (P_charger * (estimateDuration.total_seconds() / 3600)) + 10
    value = int(flexWh * 1e18)
    if value < 0:
        value = 0
    fromAddress = df_accounts[df_accounts.userID == userId].Address[0]
    startTime = (startTime - pd.Timestamp("1970-01-01", tz='UTC')) // pd.Timedelta('1s')  # to unix timestamp
    desiredWh = int(desiredkWh * 1000)
    transactionHash = contract.functions.startCharging(userId, chargerId, startTime, int(round(estimateDuration.total_seconds(), 0)),
                                                       desiredWh).transact({'from': fromAddress, 'value': value})
    web3.eth.waitForTransactionReceipt(transactionHash)
    return value, transactionHash


def stopCharging(web3, contract, df_accounts, userId, chargerId, endTime, flexFlow, chargedkWh):
    fromAddress = df_accounts[df_accounts.userID == userId].Address[0]
    endTime = (endTime - pd.Timestamp("1970-01-01", tz='UTC')) // pd.Timedelta('1s')  # to unix timestamp
    chargedWh = int(chargedkWh * 1000)
    transactionHash = contract.functions.stopCharging(userId, chargerId, endTime, flexFlow, chargedWh).transact(
        {'from': fromAddress})
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