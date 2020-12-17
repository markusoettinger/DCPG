from web3 import Web3



address = '0xDE9d2de48969B86826da4336F389c21e2d1c9812'
privateKey = '0x48bd694bbfd4f2816b4355776d3c403449d95298a0cc4835e0372447013e84de'

infura_url = 'https://ropsten.infura.io/v3/1761beb5aae7459b83afd64e8f1003fc'

web3 = Web3(Web3.HTTPProvider(infura_url))

web3.eth.defaultAccount = address;
web3.eth.wallet.add({
    privateKey: privateKey,
    address: address,
})

def create_account(web3):
    acc = web3.eth.account.create()
    return acc

def get_Balance(web3, account):
    balance = web3.eth.getBalance(account.address)
    return balance

def get_Token(web3, acc, value):
    web3.eth.sendTransaction(
        {'to': acc.address, 'from': '0xDE9d2de48969B86826da4336F389c21e2d1c9812',
         'value': value})

#acc1 = create_account(web3)
#print(acc1.address)

ret = web3.eth.sendTransaction({'to': '0x839d2Cb7a7c568a51731B2bDFA186Bd22b803F61', 'from': '0xDE9d2de48969B86826da4336F389c21e2d1c9812', 'value': 100})
print('Add some tokens please')

transaction = {
    'to': '0x839d2Cb7a7c568a51731B2bDFA186Bd22b803F61',
    'from': '0xDE9d2de48969B86826da4336F389c21e2d1c9812',
    'value': 10000,
    'gas': 2100000,
    'gasPrice': 290000020,
    'nonce': 1,
    'chainId': web3.eth.chainId
}

key = '0x48bd694bbfd4f2816b4355776d3c403449d95298a0cc4835e0372447013e84de'
signed = web3.eth.account.sign_transaction(transaction, key)
ret = web3.eth.sendRawTransaction(signed.rawTransaction)
print(Web3.toHex(ret))