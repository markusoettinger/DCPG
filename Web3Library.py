# Library with functions of the Web3 Library to connect and interact with the blockchain and smart contract on the BC

from web3 import Web3, HTTPProvider
import pandas as pd


def connect(ganache):
    if ganache:
        rpc_server = 'HTTP://127.0.0.1:7545'
    else:
        rpc_server = ganache
    web3 = Web3(HTTPProvider(rpc_server))
    web3.eth.defaultAccount(web3.eth.accounts[0])
    return web3


def getBalance(web3, address):
    return web3.eth.getBalance(address)


def transact(web3, toAddress, fromAddress, value):
    if fromAddress == 'Faucet':
        ret = web3.eth.sendTransaction({{'to': toAddress, 'value': value}})
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
        transact(web3, newAddress, 'Faucet', 8e19) # need to be changed to highest Flexpayer amount
    return web3, newAddress, df_accounts


def connectContract(web3):
    contractaddress = '0xde36d227c7Bc968905DC5d2D946F3EC98e267B2D'
    contractabi = '[{"constant": false, "inputs": [{"internalType": "uint256", "name": "num", "type": "uint256"}], "name": "store", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "retrieve", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}]'
    return web3.eth.contract(address=web3.toChecksumAddress(contractaddress), abi=contractabi)


def startCharching(web3, contract, df_accounts, userId, chargerId, startTime, estimateDuration, desiredkWh):
    P_charger = 3.5  # kW --> example for calculating max Flex to pay
    # estimateDuration evtl. umwandeln
    flexWh = desiredkWh - (P_charger * (estimateDuration / 60)) + 10
    value = flexWh * 1e18
    if value < 0:
        value = 0
    fromAddress = df_accounts[df_accounts.userID == userId].Address
    transactionHash = contract.functions.startCharching(userId, chargerId, startTime, estimateDuration,
                                                        desiredkWh).transact({'from': fromAddress, 'value': value})
    web3.eth.waitforTransactionReciept(transactionHash)
    return value, transactionHash


def stopCharching(web3, contract, df_accounts, userId, chargerId, endTime, flexFlow, charchedWh):
    fromAddress = df_accounts[df_accounts.userID == userId].Address
    transactionHash = contract.functions.stopCharging(userId, chargerId, endTime, flexFlow, charchedWh).transact(
        {'from': fromAddress})
    web3.eth.waitforTransactionReciept(transactionHash)
    return transactionHash
