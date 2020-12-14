import web3
from web3 import Web3

def connect():
    weby = Web3(Web3.HTTPProvider("https://volta-rpc.energyweb.org"))
    return weby

weby = connect()

try:
    ret=weby.eth.sendTransaction({'to': '0xDE9d2de48969B86826da4336F389c21e2d1c9812', 'from': '0xDE9d2de48969B86826da4336F389c21e2d1c9812', 'value': 1})
    print(ret)
except:
    print('failed sendTransaction')


transaction = {
    'to': '0xDE9d2de48969B86826da4336F389c21e2d1c9812',
    'from': '0xDE9d2de48969B86826da4336F389c21e2d1c9812',
    'value': 100000,
    'gas': 21020,
    'gasPrice': 29000002000,
    'nonce': 10,
    'chainId': 73799
}

signed = weby.eth.account.sign_transaction(transaction, key)
ret = weby.eth.sendRawTransaction(signed.rawTransaction)
print(ret)
print('failed sign_transaction')
