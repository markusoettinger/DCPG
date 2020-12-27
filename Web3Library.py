#Library with functions of the Web3 Library to connect and interact with the blockchain and smart contract on the BC

from web3 import Web3, HTTPProvider
import pandas as pd

def connect(ganache):
    if ganache == True:
        rpc_server = 'HTTP://127.0.0.1:7545'
    else:
        rpc_server = ganache
    web3 = Web3(HTTPProvider(rpc_server))
    return web3

def getBalance(web3, address):
    return web3.eth.getBalance(address)

def transact(web3, toAddress, fromAdress, value):
    ret = web3.eth.sendTransaction({'to': toAddress, 'from': fromAdress, 'value': value})
    return Web3.toHex(ret)

def newAccount(web3, userId, df_accounts):
    #df_accounts = pd.readcsv('accountList.csv')
    if df_accounts.iloc(userId) == []:
        newaddress = web3.geth.personal.new_account(str(userId))
        web3.geth.personal.unlockAccount(newaddress, str(userId), 0)
        df_accounts = df_accounts.append(pd.DataFrame([newaddress], index=userId))
        df_accounts.to_csv('accountList.csv')
    return web3, newaddress, df_accounts

def connectContract(web3):
    contractaddress = '0xde36d227c7Bc968905DC5d2D946F3EC98e267B2D'
    contractabi = '[{"constant": false, "inputs": [{"internalType": "uint256", "name": "num", "type": "uint256"}], "name": "store", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "retrieve", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}]'
    return web3.eth.contract(address=web3.toChecksumAddress(contractaddress), abi=contractabi)

def startCharching(web3, contract, df_accounts, userId, chargerId, startTime, estimateDuration, desiredWh):
    P_charger = 10000 #Watt --> example for calculating max Flex to pay
    #estimateDuration evtl. umwandeln
    flexWh = desiredWh - (P_charger * (estimateDuration/60))
    value = flexWh * (1e18)
    fromAddress = df_accounts.iloc(userId)
    hash = contract.functions.startCharching(userId, chargerId, startTime, estimateDuration, desiredWh).transact({'from': fromAddress, 'value': value})
    web3.eth.waitforTransactionReciept(hash)
    return

def stopCharching(web3, contract, df_accounts, userId, chargerId, endTime, flexFlow, charchedWh):
    fromAddress = df_accounts.iloc(userId)
    hash = contract.functions.stopCharging(userId, chargerId, endTime, flexFlow, charchedWh).transact({'from': fromAddress})
    web3.eth.waitforTransactionReciept(hash)
    return


