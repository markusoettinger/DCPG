# %%

from web3 import Web3


class test:
    def cooltest(self):
        return 1
#%%

weby = Web3(Web3.HTTPProvider("https://volta-rpc.energyweb.org"))

#%%

acc = weby.eth.account.create("this is a very long and cool string")
# %%


# https://www.dappuniversity.com/articles/web3-py-intro
print(web3.eth.blockNumber)
print(web3.fromWei(balance, "ether"))


abi = [
    {
        "constant": true,
        "inputs": [],
        "name": "mintingFinished",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": true,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": false,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [],
        "payable": false,
        "type": "function",
    },
    {
        "constant": true,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": false,
        "inputs": [
            {"name": "_from", "type": "address"},
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [],
        "payable": false,
        "type": "function",
    },
    {
        "constant": true,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": false,
        "inputs": [],
        "name": "unpause",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": false,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_amount", "type": "uint256"},
        ],
        "name": "mint",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": true,
        "inputs": [],
        "name": "paused",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": true,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": false,
        "inputs": [],
        "name": "finishMinting",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": false,
        "inputs": [],
        "name": "pause",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": true,
        "inputs": [],
        "name": "owner",
        "outputs": [{"name": "", "type": "address"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": true,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": false,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [],
        "payable": false,
        "type": "function",
    },
    {
        "constant": false,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_amount", "type": "uint256"},
            {"name": "_releaseTime", "type": "uint256"},
        ],
        "name": "mintTimelocked",
        "outputs": [{"name": "", "type": "address"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": true,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"name": "remaining", "type": "uint256"}],
        "payable": false,
        "type": "function",
    },
    {
        "constant": false,
        "inputs": [{"name": "newOwner", "type": "address"}],
        "name": "transferOwnership",
        "outputs": [],
        "payable": false,
        "type": "function",
    },
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "name": "to", "type": "address"},
            {"indexed": false, "name": "value", "type": "uint256"},
        ],
        "name": "Mint",
        "type": "event",
    },
    {"anonymous": false, "inputs": [], "name": "MintFinished", "type": "event"},
    {"anonymous": false, "inputs": [], "name": "Pause", "type": "event"},
    {"anonymous": false, "inputs": [], "name": "Unpause", "type": "event"},
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "name": "owner", "type": "address"},
            {"indexed": true, "name": "spender", "type": "address"},
            {"indexed": false, "name": "value", "type": "uint256"},
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "anonymous": false,
        "inputs": [
            {"indexed": true, "name": "from", "type": "address"},
            {"indexed": true, "name": "to", "type": "address"},
            {"indexed": false, "name": "value", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    },
]

contract = web3.eth.contract(address=address, abi=abi)


totalSupply = contract.functions.totalSupply().call()
print(web3.fromWei(totalSupply, 'ether'))

# from web3 import Web3, HTTPProvider


# From https://subscription.packtpub.com/book/big_data_and_business_intelligence/9781788627856/4/ch04lvl1sec36/understanding-the-web3-py-library
# w3 = Web3(HTTPProvider('http://localhost:7545'))

# private_key = '59e31694256f71b8d181f47fc67914798c4b96990e835fc1407bf4673ead30e2'

# transaction = {
#   'to': Web3.toChecksumAddress('0x9049386D4d5808e0Cd9e294F2aA3d70F01Fbf0C5'),
#   'value': w3.toWei('1', 'ether'),
#   'gas': 100000,
#   'gasPrice': w3.toWei('1', 'gwei'),
#   'nonce': 0
# }

# signed = w3.eth.account.signTransaction(transaction, private_key)
# tx = w3.eth.sendRawTransaction(signed.rawTransaction)
