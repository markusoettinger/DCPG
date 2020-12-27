from web3 import Web3, HTTPProvider

CONTRACTADDRESS = '0xde36d227c7Bc968905DC5d2D946F3EC98e267B2D'
CONTRACTABI = '[{"constant": false, "inputs": [{"internalType": "uint256", "name": "num", "type": "uint256"}], "name": "store", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function"}, {"constant": true, "inputs": [], "name": "retrieve", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"}]'
ganache_rpc_server = 'HTTP://127.0.0.1:7545'

web3 = Web3(HTTPProvider(ganache_rpc_server))

# balance = web3.eth.getBalance('0x5494408D1A30E9c9cAcf4cDE5Aa62fB2552B4A13')
#
# print(balance)
#
# ret = web3.eth.sendTransaction({'to': web3.eth.accounts[0], 'from': web3.eth.accounts[1], 'value': 100000})
#
# print(Web3.toHex(ret))
#
# newaddress = web3.geth.personal.new_account('hallo')
# print(newaddress)
# web3.geth.personal.unlockAccount(newaddress, 'hallo', 0)

# ret = web3.eth.sendTransaction({'from': web3.eth.accounts[1], 'to': newaddress, 'value': 1000000000000002000})
# print(Web3.toHex(ret))
# ret = web3.eth.sendTransaction({'to': web3.eth.accounts[1], 'from': newaddress, 'value': 10000000000000020})

web3.eth.defaultAccount = web3.eth.accounts[0]

contract = web3.eth.contract(address=web3.toChecksumAddress(CONTRACTADDRESS), abi=CONTRACTABI)

contract.functions.store(2020).transact()

contract.functions.store(2020).transact({'from': web3.eth.accounts[2], 'value': 1000000})

retuning = contract.functions.retrieve().call()

print(retuning)

