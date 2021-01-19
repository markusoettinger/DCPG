InfuraProjectId = '1761beb5aae7459b83afd64e8f1003fc'

import os

os.environ['WEB3_INFURA_PROJECT_ID'] = InfuraProjectId

from web3.auto.infura import w3
print(w3.isConnected())

address = '0xDE9d2de48969B86826da4336F389c21e2d1c9812'
privateKey = '0x48bd694bbfd4f2816b4355776d3c403449d95298a0cc4835e0372447013e84de'
w3.eth.defaultAccount = address
w3.eth.account.privateKeyToAccount(privateKey)


ret = w3.eth.sendTransaction({'to': '0x839d2Cb7a7c568a51731B2bDFA186Bd22b803F61', 'value': 100})

w3.eth.accounts.wallet.add({
    address: address,
    privateKey: privateKey
})