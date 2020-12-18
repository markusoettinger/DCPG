from web3 import Web3, HTTPProvider

ganache_rpc_server = 'HTTP://127.0.0.1:7545'

web3 = Web3(HTTPProvider(ganache_rpc_server))

balance = web3.eth.getBalance('0x5494408D1A30E9c9cAcf4cDE5Aa62fB2552B4A13')

print(balance)

ret = web3.eth.sendTransaction({'to': web3.eth.accounts[0], 'from': web3.eth.accounts[1], 'value': 100000})

print(Web3.toHex(ret))

acc = web3.eth.account.create()

print(acc.address)

