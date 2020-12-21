from web3 import Web3, HTTPProvider

ganache_rpc_server = 'HTTP://127.0.0.1:7545'

web3 = Web3(HTTPProvider(ganache_rpc_server))

balance = web3.eth.getBalance('0x5494408D1A30E9c9cAcf4cDE5Aa62fB2552B4A13')

print(balance)

ret = web3.eth.sendTransaction({'to': web3.eth.accounts[0], 'from': web3.eth.accounts[1], 'value': 100000})

print(Web3.toHex(ret))

newaddress = web3.geth.personal.new_account('hallo')
print(newaddress)
web3.geth.personal.unlockAccount(newaddress, 'hallo', 0)

ret = web3.eth.sendTransaction({'from': web3.eth.accounts[1], 'to': newaddress, 'value': 1000000000000002000})
print(Web3.toHex(ret))
ret = web3.eth.sendTransaction({'to': web3.eth.accounts[1], 'from': newaddress, 'value': 10000000000000020})

