from web3 import Web3
import pytest

# https://web3py.readthedocs.io/en/stable/web3.eth.html

@pytest.fixture
def connect():
    weby = Web3(Web3.HTTPProvider("https://volta-rpc.energyweb.org"))
    return weby


def test_connect(connect):
    weby = connect
    assert weby.isConnected() == True

def test_getBlock(connect):
    weby = connect
    some_block = weby.eth.getBlock(9513812)
    # Found on https://volta-explorer.energyweb.org/blocks/9513812/transactions
    assert (
        some_block.hash.hex()
        == "0x416e791908265e2c758d68f515c5ebada4cffff17499ab3a2c74549e72aa467e"
    )

# def test_transaction(connect):
#     weby = connect

#     some_block = weby.getTransaction()
#     # Found on https://volta-explorer.energyweb.org/blocks/9513812/transactions
#     assert (
#         some_block.hash.hex()
#         == "0x416e791908265e2c758d68f515c5ebada4cffff17499ab3a2c74549e72aa467e"
#     )


# https://web3py.readthedocs.io/en/stable/web3.eth.account.html#eth-account
# mhh mal sehen was das soll

def test_accounts(connect):
    weby = connect 

    print(weby.eth.accounts)

    assert (True)

#>>> web3.eth.sendTransaction({'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601', 'from': web3.eth.coinbase, 'value': 12345})
#0xe670ec64341771606e55d6b4ca35a1a6b75ee3d5145a99d05921026d1527331'

# >>> web3.eth.estimateGas({'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601', 'from': web3.eth.coinbase, 'value': 12345})
# 21000

#from web3 import Web3

# w3 = Web3(...)

# contract = w3.eth.contract(address='0x000000000000000000000000000000000000dEaD', abi=...)

# # alternatively:
# contract = w3.eth.contract(address='mycontract.eth', abi=...)

def test_balance(connect): # This test fails.. it says that it can not get b
    weby = connect
    wallet_id = weby.toChecksumAddress('0xD5663B3169F0E6DD50A01AA680760080433BC333')
    balance = weby.eth.getBalance(wallet_id)

    assert(balance == 2000000000000000000)


if __name__ == "__main__":
    weby = Web3(Web3.HTTPProvider("https://volta-rpc.energyweb.org"))
    print(weby.eth.accounts)
    pass

