import web3
from web3 import Web3, HTTPProvider

def connect():
    weby = Web3(HTTPProvider("https://volta-rpc.energyweb.org"))
    return weby

weby = connect()

ret=weby.eth.sendTransaction({'to': '0xDE9d2de48969B86826da4336F389c21e2d1c9812', 'from': '0xDE9d2de48969B86826da4336F389c21e2d1c9812', 'value': 1})
print(ret)


transaction = {
    'to': '0xDE9d2de48969B86826da4336F389c21e2d1c9812',
    'from': '0xDE9d2de48969B86826da4336F389c21e2d1c9812',
    'value': 10000,
    'gas': 2100000,
    'gasPrice': 290000020,
    'nonce': 9,
    'chainId': 73799
}
key = '0x48bd694bbfd4f2816b4355776d3c403449d95298a0cc4835e0372447013e84de'
signed = weby.eth.account.sign_transaction(transaction, key)
ret = weby.eth.sendRawTransaction(signed.rawTransaction)
print(Web3.toHex(ret))

